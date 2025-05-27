import os
import re

import pytest

from src.authors_client import AuthorsClient
from src.base_client import BaseClient
from src.books_client import BooksClient
from utils.path_resolver import ROOT_DIR


@pytest.fixture(scope="session")
def base_url() -> str:
    return os.getenv("BOOKSTORE_API_URL", "https://fakerestapi.azurewebsites.net")


@pytest.fixture(scope="session")
def client(base_url) -> BaseClient:
    return BaseClient(base_url)


@pytest.fixture(scope="session")
def books_client(base_url) -> BooksClient:
    return BooksClient(BaseClient(base_url))


@pytest.fixture(scope="session")
def authors_client(base_url) -> AuthorsClient:
    return AuthorsClient(BaseClient(base_url))


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """
    Pytest configure hook to define an HTML report
    """
    config.option.htmlpath = f"{ROOT_DIR}/report.html"


@pytest.hookimpl(optionalhook=True)
def pytest_html_results_table_header(cells):
    """
    Adds columns for Test ID, Description, and Feature to the HTML report header
    """
    cells.insert(2, '<th class="sortable" data-column-type="test_id">ID</th>')
    cells.insert(3, '<th class="sortable" data-column-type="description">Description</th>')
    cells.insert(4, '<th class="sortable" data-column-type="type">Feature</th>')


@pytest.hookimpl(optionalhook=True)
def pytest_html_results_table_row(report, cells):
    """
    Populates each row with the Test ID, Description, and Feature values
    """
    cells.insert(2, f'<td class="col-test_id">{getattr(report, "test_id", "N/A")}</td>')
    cells.insert(3, f'<td class="col-description">{getattr(report, "description", "Not provided")}</td>')
    cells.insert(4, f'<td class="col-type">{getattr(report, "feature", "Unmarked")}</td>')


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Attaches metadata (test_id, description, feature) to the report object
    """
    outcome = yield
    report = outcome.get_result()

    # Get marker if used
    marker = item.get_closest_marker("test_details")

    # Test ID: from marker.args or marker.kwargs['test_id'] or fallback to docstring
    if marker:
        # support @pytest.mark.test_details("", description=..., feature=...)
        report.test_id = marker.kwargs.get("test_id", marker.args[0] if marker.args else "N/A")
    else:
        doc = item.function.__doc__ or ""
        first_line = doc.strip().splitlines()[0] if doc.strip() else ""
        match = re.match(r'^([A-Z]+-\d+)', first_line)
        report.test_id = match.group(1) if match else "N/A"

    # Description: prefer marker.kwargs['description'], then docstring minus ID
    if marker and "description" in marker.kwargs:
        report.description = marker.kwargs["description"]
    else:
        doc = item.function.__doc__ or ""
        text = doc.strip()
        if text.startswith(report.test_id):
            report.description = text[len(report.test_id):].strip()
        else:
            report.description = text
        if not report.description:
            report.description = "Not provided"

    # Test Type: prefer marker.kwargs['feature'], else other markers
    if marker and "feature" in marker.kwargs:
        report.feature = marker.kwargs["feature"]
    else:
        types = []
        for m in item.iter_markers():
            if m.name in ["books", "authors"]:
                types.append(m.name.capitalize())
        report.feature = ", ".join(types) if types else "Unmarked"
