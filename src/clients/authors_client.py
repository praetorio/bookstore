from configs.bookstore_resource import BookstoreResource
from src.clients.base_resoruces_client import BaseResourceClient


class AuthorsClient(BaseResourceClient):
    _resource = BookstoreResource.AUTHORS
    