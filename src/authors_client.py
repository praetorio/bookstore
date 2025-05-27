from configs.bookstore_resource import BookstoreResource
from src.base_resoruces_client import BaseResourceClient


class AuthorsClient(BaseResourceClient):
    _resource = BookstoreResource.AUTHORS
    