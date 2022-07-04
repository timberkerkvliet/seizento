import os
from multiprocessing import Process
from time import sleep

import requests


class E2ETestClient:
    def __enter__(self):
        self.process = Process(target=os.system, args=('python3 -m uvicorn app:app',))
        self.process.start()
        sleep(1)

    def __exit__(self):
        self.process.kill()

    def get(self, resource: str):
        return requests.get(url='http://localhost:8000' + resource).json()

    def set(self, resource: str, data):
        requests.put(url='http://localhost:8000' + resource, json=data)

    def delete(self, resource: str) -> None:
        requests.delete(url='http://localhost:8000' + resource)
