from typing import Optional, Union

import requests


class TestClient:
    ADMIN_TOKEN = 'admin'

    def __init__(self, host: str):
        self._host = host

    def post(self, url: str, data: dict, token: Optional[str] = None):
        requests.post(
            url=self._host + url,
            json=data,
            headers={f'Bearer {token or self.ADMIN_TOKEN}'}
        )

    def get(self, url: str, token: Optional[str] = None):
        resp = requests.get(
            url=self._host + url,
            headers={f'Bearer {token or self.ADMIN_TOKEN}'}
        )

        return resp.json()

    def put(self, url: str, data: Union[str, int, list, dict], token: Optional[str] = None):
        requests.put(
            url=self._host + url,
            json=data,
            headers={f'Bearer {token or self.ADMIN_TOKEN}'}
        )

    def patch(self, url: str, data: Union[str, int, list, dict], token: Optional[str] = None):
        requests.patch(
            url=self._host + url,
            json=data,
            headers={f'Bearer {token or self.ADMIN_TOKEN}'}
        )
