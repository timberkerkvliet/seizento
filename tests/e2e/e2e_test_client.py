import os
from multiprocessing import Process
from time import sleep

import requests


class E2ETestClient:
    def __init__(self):
        self.token = None

    def __enter__(self):
        self.process = Process(target=os.system, args=('python3 -m uvicorn --port 8003 starlette_app:starlette_app',))
        self.process.start()
        sleep(0.5)

    def __exit__(self):
        self.process.kill()

    def login(self, data=None):
        data = data or {'user_id': 'admin', 'password': 'admin'}

        self.token = requests.post(
            url='http://localhost:8003/login',
            json=data
        ).json()

    def get(self, resource: str):
        if self.token is None:
            self.login()
        return requests.get(
            url='http://localhost:8003' + resource,
            headers={'Authorization': f'Bearer {self.token}'}
        ).json()

    def set(self, resource: str, data):
        if self.token is None:
            self.login()
        requests.put(
            url='http://localhost:8003' + resource,
            headers={'Authorization': f'Bearer {self.token}'},
            json=data
        )

    def delete(self, resource: str) -> None:
        if self.token is None:
            self.login()
        requests.delete(
            url='http://localhost:8003' + resource,
            headers={'Authorization': f'Bearer {self.token}'}
        )
