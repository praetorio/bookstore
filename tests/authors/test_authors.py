from http import HTTPStatus

import pytest
from jsonschema import validate
from src.schemas import AUTHOR_SCHEMA, AUTHOR_LIST_SCHEMA, ERROR_SCHEMA
from tests.data.author_test_data import AUTHOR_PAYLOAD, INVALID_AUTHOR_PAYLOAD


@pytest.mark.authors
@pytest.mark.test_details("AUTHOR-01", description="List all authors", feature="AUTHORS")
def test_list_authors(authors_client):
    status_code, authors = authors_client.list()
    assert status_code == HTTPStatus.OK, f"Expected {HTTPStatus.OK}, got {status_code}."
    validate(authors, AUTHOR_LIST_SCHEMA)


@pytest.mark.authors
@pytest.mark.test_details("AUTHOR-02", description="Retrieve an author by valid ID", feature="AUTHORS")
def test_get_author(authors_client):
    status_code, author = authors_client.get(1)
    assert status_code == HTTPStatus.OK, f"Expected {HTTPStatus.OK}, got {status_code}."
    validate(author, AUTHOR_SCHEMA)


@pytest.mark.authors
@pytest.mark.test_details("AUTHOR-03", description="Retrieve an author by invalid/non-existent ID", feature="AUTHORS")
def test_get_author_invalid(authors_client):
    status_code, author = authors_client.get(1000)
    assert status_code == HTTPStatus.NOT_FOUND, f"Expected {HTTPStatus.NOT_FOUND}, got {status_code}."
    validate(author, ERROR_SCHEMA)


@pytest.mark.authors
@pytest.mark.test_details("AUTHOR-04", description="Create an author with valid payload", feature="AUTHORS")
def test_create_author(authors_client):
    status_code, author = authors_client.create(AUTHOR_PAYLOAD)
    # Based on the API documentation, the expected status code for creation is 200 OK, but I would expect 201 Created.
    assert status_code == HTTPStatus.OK, f"Expected {HTTPStatus.OK}, got {status_code}."
    validate(author, AUTHOR_SCHEMA)


@pytest.mark.authors
@pytest.mark.test_details("AUTHOR-05", description="Create an author with wrong data types", feature="AUTHORS")
def test_create_author_invalid(authors_client):
    status_code, author = authors_client.create(INVALID_AUTHOR_PAYLOAD)
    assert status_code == HTTPStatus.BAD_REQUEST, f"Expected {HTTPStatus.BAD_REQUEST}, got {status_code}."
    validate(author, ERROR_SCHEMA)


@pytest.mark.authors
@pytest.mark.test_details("AUTHOR-06", description="Create an author missing a required field", feature="AUTHORS")
def test_create_author_invalid_missing_id(authors_client):
    status_code, author = authors_client.create(INVALID_AUTHOR_PAYLOAD)
    assert status_code == HTTPStatus.BAD_REQUEST, f"Expected {HTTPStatus.BAD_REQUEST}, got {status_code}."
    validate(author, ERROR_SCHEMA)


@pytest.mark.authors
@pytest.mark.test_details("AUTHOR-07", description="Update an existing author with valid payload", feature="AUTHORS")
def test_update_author(authors_client):
    status_code, author = authors_client.update(1, AUTHOR_PAYLOAD)
    assert status_code == HTTPStatus.OK, f"Expected {HTTPStatus.OK}, got {status_code}."
    validate(author, AUTHOR_SCHEMA)


@pytest.mark.authors
@pytest.mark.test_details("AUTHOR-08", description="Update a non-existent author", feature="AUTHORS")
def test_update_author_invalid(authors_client):
    status_code, author = authors_client.update(1000, AUTHOR_PAYLOAD)
    assert status_code == HTTPStatus.NOT_FOUND, f"Expected {HTTPStatus.NOT_FOUND}, got {status_code}."
    validate(author, ERROR_SCHEMA)


@pytest.mark.authors
@pytest.mark.test_details("AUTHOR-09", description="Update an author with malformed payload", feature="AUTHORS")
def test_update_author_invalid_payload(authors_client):
    status_code, author = authors_client.update(1, INVALID_AUTHOR_PAYLOAD)
    assert status_code == HTTPStatus.BAD_REQUEST, f"Expected {HTTPStatus.BAD_REQUEST}, got {status_code}."
    validate(author, ERROR_SCHEMA)


@pytest.mark.authors
@pytest.mark.test_details("AUTHOR-10", description="Delete an existing author", feature="AUTHORS")
def test_delete_author(authors_client):
    status_code = authors_client.delete(1)
    # Based on the API documentation, the expected status code for deletion is 200 OK, but I would expect 204 No Content
    assert status_code == HTTPStatus.OK, f"Expected {HTTPStatus.OK}, got {status_code}."


@pytest.mark.authors
@pytest.mark.test_details("AUTHOR-11", description="Delete a non-existent author", feature="AUTHORS")
def test_delete_author_invalid(authors_client):
    status_code = authors_client.delete(1000)
    # Based on the API documentation, the expected status code for deletion is 200 OK, but I would expect 204 No Content
    assert status_code == HTTPStatus.OK, f"Expected {HTTPStatus.OK}, got {status_code}."


@pytest.mark.authors
@pytest.mark.test_details("AUTHOR-12", description="CRUD operations on author schema", feature="AUTHORS")
def test_crud_author_schema(authors_client):
    # create
    status_code, created = authors_client.create(AUTHOR_PAYLOAD)
    assert status_code == HTTPStatus.OK, f"Expected to create author, got {status_code}."
    validate(created, AUTHOR_SCHEMA)
    author_id = created["id"]

    # read
    status_code, fetched = authors_client.get(author_id)
    assert status_code == HTTPStatus.OK, f"Expected to retrieve author, got {status_code}."
    validate(fetched, AUTHOR_SCHEMA)

    # update
    updated_payload = {**AUTHOR_PAYLOAD, "firstName": "John"}
    status_code, updated = authors_client.update(author_id, updated_payload)
    assert status_code == HTTPStatus.OK, f"Expected to update author, got {status_code}."
    validate(updated, AUTHOR_SCHEMA)
    assert updated["firstName"] == "John", f"Expected firstName to be updated to 'John', got {updated['firstName']}."

    # delete
    status_code = authors_client.delete(author_id)
    assert status_code == HTTPStatus.OK, f"Expected to delete author, got {status_code}."
    status_code, _ = authors_client.get(author_id)
    assert status_code == HTTPStatus.NOT_FOUND, f"Expected author to be deleted, got {status_code}."
