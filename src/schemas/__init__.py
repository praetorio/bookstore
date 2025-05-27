from src.schemas.authors_schemas import AUTHOR_SCHEMA, AUTHOR_LIST_SCHEMA
from src.schemas.books_schemas import BOOK_SCHEMA, BOOK_LIST_SCHEMA
from src.schemas.common_schemas import ERROR_SCHEMA


def book_schema():
    return BOOK_SCHEMA


def book_list_schema():
    return BOOK_LIST_SCHEMA


def author_schema():
    return AUTHOR_SCHEMA


def author_list_schema():
    return AUTHOR_LIST_SCHEMA


def invalid_schema():
    return ERROR_SCHEMA
