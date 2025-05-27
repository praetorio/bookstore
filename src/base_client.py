from http import HTTPStatus
from typing import Optional, Dict, Any, Set, Tuple

from configs.wait_type import WaitType
from utils.singleton_meta import Singleton

import requests


class BookstoreClient(metaclass=Singleton):
    def __init__(self, base_url: str):
        self.base = base_url.rstrip("/")
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json",
        })

    def _request(self, method: str, path: str, *, json: Optional[Dict[str, Any]] = None, expected: Set[HTTPStatus] = None) -> Tuple[HTTPStatus, Any]:
        url = f"{self.base}{path}"
        resp = self.session.request(method=method, url=url, json=json, timeout=WaitType.DEFAULT.value)
        status = HTTPStatus(resp.status_code)
        if status not in expected:
            resp.raise_for_status()
        if status == HTTPStatus.NO_CONTENT or not resp.content:
            return status, None
        return status, resp.json()