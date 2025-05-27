from http import HTTPStatus, HTTPMethod
from typing import Type, Dict, Any, Tuple, List

from configs.bookstore_resource import BookstoreResource
from src.clients.base_client import BaseClient


class BaseResourceClient:
    """
    Generic resource wrapper that knows how to do GET/POST/PUT/DELETE against /api/v1/{resource}.
    """
    _resource: BookstoreResource

    def __init__(self, client: BaseClient):
        self._client = client
        self._path = f"/api/v1/{self._resource}"

    def list(self) -> Tuple[HTTPStatus, List[Dict[str, Any]]]:
        return self._client.request(HTTPMethod.GET, self._path, expected={HTTPStatus.OK})

    def get(self, item_id: int) -> Tuple[HTTPStatus, Dict[str, Any]]:
        return self._client.request(HTTPMethod.GET, f"{self._path}/{item_id}",
                                    expected={HTTPStatus.OK, HTTPStatus.NOT_FOUND})

    def create(self, payload: Dict[str, Any]) -> Tuple[HTTPStatus, Dict[str, Any]]:
        return self._client.request(HTTPMethod.POST, self._path, json=payload, expected={HTTPStatus.CREATED, HTTPStatus.BAD_REQUEST})

    def update(self, item_id: int, payload: Dict[str, Any]) -> Tuple[HTTPStatus, Dict[str, Any]]:
        return self._client.request(HTTPMethod.PUT, f"{self._path}/{item_id}", json=payload,
                                    expected={HTTPStatus.OK, HTTPStatus.NOT_FOUND, HTTPStatus.BAD_REQUEST})

    def delete(self, item_id: int) -> HTTPStatus:
        status, _ = self._client.request(HTTPMethod.DELETE, f"{self._path}/{item_id}",
                                         expected={HTTPStatus.NO_CONTENT, HTTPStatus.NOT_FOUND})
        return status


def resource_client_factory(cls: Type[BaseResourceClient], client: BaseClient) -> BaseResourceClient:
    return cls(client)
