# NOTE: Filename is intentionally wrong (without 'test_' prefix) to exclude it from automatic test discovery.
import pytest
from http import HTTPStatus
from jsonschema import validate
from src.schemas import BOOK_SCHEMA, BOOK_LIST_SCHEMA, ERROR_SCHEMA


BOOK_PAYLOAD = {
    "id": 999,
    "title": "Pytest JSON-Schema Demo",
    "description": "Testing JSON schema validation",
    "pageCount": 0,
    "excerpt": "Once upon a test…",
    "publishDate": "2025-05-27T00:00:00Z"
}

INVALID_BOOK_PAYLOAD = {
    "id": 0,
    "title": "Pytest JSON-Schema Demo",
    "description": "Testing JSON schema validation",
    "pageCount": "ZERO",  # bad type
    "excerpt": "Once upon a test…",
    "publishDate": "2025-05-27T00:00:00Z"
}


@pytest.mark.books
@pytest.mark.parametrize(
    "method,args,expected_status,schema",
    [
        ("list", (), HTTPStatus.OK, BOOK_LIST_SCHEMA),
        ("get",  (1,), HTTPStatus.OK,  BOOK_SCHEMA),
        ("get",  (1000,), HTTPStatus.NOT_FOUND, ERROR_SCHEMA),
    ],
)
def test_list_and_get(method, args, expected_status, schema, books_client):
    status, body = getattr(books_client, method)(*args)
    assert status == expected_status, f"{method}(*{args}) returned {status}"
    validate(body, schema)


@pytest.mark.books
@pytest.mark.parametrize(
    "payload,expected_status,expected_schema",
    [
        (BOOK_PAYLOAD,         HTTPStatus.OK,          BOOK_SCHEMA),
        (INVALID_BOOK_PAYLOAD, HTTPStatus.BAD_REQUEST, ERROR_SCHEMA),
    ],
)
def test_create_book_validation(payload, expected_status, expected_schema, books_client):
    status, body = books_client.create(payload)
    assert status == expected_status, f"create({payload}) returned {status}"
    validate(body, expected_schema)


@pytest.mark.books
@pytest.mark.parametrize(
    "book_id,payload,expected_status,expected_schema",
    [
        (1,    BOOK_PAYLOAD,         HTTPStatus.OK,          BOOK_SCHEMA),
        (1000, BOOK_PAYLOAD,         HTTPStatus.NOT_FOUND,   ERROR_SCHEMA),
        (1,    INVALID_BOOK_PAYLOAD, HTTPStatus.BAD_REQUEST, ERROR_SCHEMA),
    ],
)
def test_update_book_validation(book_id, payload, expected_status, expected_schema, books_client):
    status, body = books_client.update(book_id, payload)
    assert status == expected_status, f"update({book_id},…) returned {status}"
    validate(body, expected_schema)


@pytest.mark.books
@pytest.mark.parametrize(
    "book_id,expected_status",
    [
        (1,    HTTPStatus.OK),
        (1000, HTTPStatus.OK),  # per current API behavior
    ],
)
def test_delete_book(book_id, expected_status, books_client):
    status = books_client.delete(book_id)
    assert status == expected_status, f"delete({book_id}) returned {status}"
