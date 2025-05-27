from http import HTTPStatus
from typing import Optional, Dict, Any, Set, Tuple

import requests

from configs.wait_type import WaitType
from utils.singleton_meta import Singleton


class BaseClient(metaclass=Singleton):
    def __init__(self, base_url: str):
        self.base = base_url.rstrip("/")
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json", "Content-Type": "application/json", })

    def request(self, method: str, path: str, *, json: Optional[Dict[str, Any]] = None,
                 expected: Set[HTTPStatus] = None) -> Tuple[HTTPStatus, Any]:
        url = f"{self.base}{path}"
        response = self.session.request(method=method, url=url, json=json, timeout=WaitType.DEFAULT.value)
        status = HTTPStatus(response.status_code)
        if HTTPStatus(response.status_code) not in expected:
            response.raise_for_status()
        if status == HTTPStatus.NO_CONTENT or not response.content:
            return status, None
        return status, response.json()