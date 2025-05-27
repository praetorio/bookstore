from configs.bookstore_resource import BookstoreResource
from src.clients.base_resoruces_client import BaseResourceClient


class BooksClient(BaseResourceClient):
    _resource = BookstoreResource.BOOKS
