from http import HTTPStatus

import pytest
from jsonschema import validate
from src.schemas import BOOK_SCHEMA, BOOK_LIST_SCHEMA, ERROR_SCHEMA
from tests.books.parametrized_test_example import INVALID_BOOK_PAYLOAD
from tests.data.book_test_data import BOOK_PAYLOAD


@pytest.mark.books
@pytest.mark.test_details("BOOK-01", description="List all books", feature="BOOKS")
def test_list_books(books_client):
    status_code, books = books_client.list()
    assert status_code == HTTPStatus.OK, f"Expected {HTTPStatus.OK}, got {status_code}."
    validate(books, BOOK_LIST_SCHEMA)


@pytest.mark.books
@pytest.mark.test_details("BOOK-02", description="Retrieve a book by valid ID", feature="BOOKS")
def test_get_book(books_client):
    status_code, books = books_client.get(1)
    assert status_code == HTTPStatus.OK, f"Expected {HTTPStatus.OK}, got {status_code}."
    validate(books, BOOK_SCHEMA)


@pytest.mark.books
@pytest.mark.test_details("BOOK-03", description="Retrieve a book by invalid/non-existent ID", feature="BOOKS")
def test_get_book_invalid(books_client):
    status_code, books = books_client.get(1000)
    assert status_code == HTTPStatus.NOT_FOUND, f"Expected {HTTPStatus.NOT_FOUND}, got {status_code}."
    validate(books, ERROR_SCHEMA)


@pytest.mark.books
@pytest.mark.test_details("BOOK-04", description="Create a book with valid payload", feature="BOOKS")
def test_create_book(books_client):
    status_code, book = books_client.create(BOOK_PAYLOAD)
    # Based on the API documentation, the expected status code for creation is 200 OK, but I would expect 201 Created.
    assert status_code == HTTPStatus.OK, f"Expected {HTTPStatus.OK}, got {status_code}."
    validate(book, BOOK_SCHEMA)


@pytest.mark.books
@pytest.mark.test_details("BOOK-05", description="Create a book with wrong data types", feature="BOOKS")
def test_create_book_invalid(books_client):
    status_code, book = books_client.create(INVALID_BOOK_PAYLOAD)
    assert status_code == HTTPStatus.BAD_REQUEST, f"Expected {HTTPStatus.BAD_REQUEST}, got {status_code}."
    validate(book, ERROR_SCHEMA)


@pytest.mark.books
@pytest.mark.test_details("BOOK-06", description="Create a book missing a required field", feature="BOOKS")
def test_create_book_invalid_missing_id(books_client):
    status_code, book = books_client.create(INVALID_BOOK_PAYLOAD)
    assert status_code == HTTPStatus.BAD_REQUEST, f"Expected {HTTPStatus.BAD_REQUEST}, got {status_code}."
    validate(book, ERROR_SCHEMA)


@pytest.mark.books
@pytest.mark.test_details("BOOK-07", description="Update an existing book with valid payload", feature="BOOKS")
def test_update_book(books_client):
    status_code, book = books_client.update(1, BOOK_PAYLOAD)
    assert status_code == HTTPStatus.OK, f"Expected {HTTPStatus.OK}, got {status_code}."
    validate(book, BOOK_SCHEMA)


@pytest.mark.books
@pytest.mark.test_details("BOOK-08", description="Update a non-existing book", feature="BOOKS")
def test_update_book_invalid(books_client):
    status_code, book = books_client.update(1000, BOOK_PAYLOAD)
    assert status_code == HTTPStatus.NOT_FOUND, f"Expected {HTTPStatus.NOT_FOUND}, got {status_code}."
    validate(book, ERROR_SCHEMA)


@pytest.mark.books
@pytest.mark.test_details("BOOK-09", description="Update a book with malformed payload", feature="BOOKS")
def test_update_book_invalid_payload(books_client):
    status_code, book = books_client.update(1, INVALID_BOOK_PAYLOAD)
    assert status_code == HTTPStatus.BAD_REQUEST, f"Expected {HTTPStatus.BAD_REQUEST}, got {status_code}."
    validate(book, ERROR_SCHEMA)


@pytest.mark.books
@pytest.mark.test_details("BOOK-10", description="Delete an existing book", feature="BOOKS")
def test_delete_book(books_client):
    status_code = books_client.delete(1)
    # Based on the API documentation, the expected status code for deletion is 200 OK, but I would expect 204 No Content
    assert status_code == HTTPStatus.OK, f"Expected {HTTPStatus.OK}, got {status_code}."


@pytest.mark.books
@pytest.mark.test_details("BOOK-11", description="Delete a non-existent book", feature="BOOKS")
def test_delete_book_invalid(books_client):
    status_code = books_client.delete(1000)
    # Based on the API documentation, the expected status code for deletion is 200 OK, but I would expect 204 No Content
    assert status_code == HTTPStatus.OK, f"Expected {HTTPStatus.OK}, got {status_code}."


@pytest.mark.books
@pytest.mark.test_details("BOOK-12", description="CRUD operations on book schema", feature="BOOKS")
def test_crud_book_schema(books_client):
    # create
    status_code, created = books_client.create(BOOK_PAYLOAD)
    assert status_code == HTTPStatus.OK, f"Expected to create book, got {status_code}."
    validate(created, BOOK_SCHEMA)
    book_id = created["id"]

    # read
    status_code, fetched = books_client.get(book_id)
    assert status_code == HTTPStatus.OK, f"Expected to retrieve book, got {status_code}."
    validate(fetched, BOOK_SCHEMA)

    # update
    updated_payload = {**BOOK_PAYLOAD, "title": "Updated Book Title"}
    status_code, updated = books_client.update(book_id, updated_payload)
    assert status_code == HTTPStatus.OK, f"Expected to update book, got {status_code}."
    validate(updated, BOOK_SCHEMA)
    assert updated["title"] == f"Expected title to be updated to 'Updated Book Title', got {updated['title']}."

    # delete
    status_code = books_client.delete(book_id)
    assert status_code == HTTPStatus.OK, f"Expected to delete book, got {status_code}."
    status_code, _ = books_client.get(book_id)
    assert status_code == HTTPStatus.NOT_FOUND, f"Expected book to be deleted, got {status_code}."
