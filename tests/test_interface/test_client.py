import os
import uuid
from multiprocessing import Process
from time import sleep
from urllib.parse import urljoin

import requests
from abc import ABC, abstractmethod

from seizento.adapters.fake_data_tree_store import FakeDataTreeStore
from seizento.controllers.resource_controller import ResourceController
from seizento.repository import Repository


class TestClient(ABC):
    @abstractmethod
    async def get(self, resource: str):
        pass

    @abstractmethod
    async def set(self, resource: str, data):
        pass

    @abstractmethod
    async def delete(self, resource: str) -> None:
        pass


class UnitTestClient(TestClient):
    ADMIN_TOKEN = 'admin'

    def __init__(self):
        store = FakeDataTreeStore()
        self.controller = ResourceController(
            repository_factory=lambda: Repository(store.get_transaction()),
            user_id=uuid.uuid4()
        )

    async def get(self, resource: str):
        return await self.controller.get(resource=resource)

    async def set(self, resource: str, data):
        await self.controller.set(resource=resource, data=data)

    async def delete(self, resource: str) -> None:
        await self.controller.delete(resource=resource)


class E2ETestClient(TestClient):
    ADMIN_TOKEN = 'admin'

    def __init__(self):
        self.started_server = False

    def _start_server(self):
        self.process = Process(target=os.system, args=('python3 -m uvicorn app:app',))
        self.process.start()
        sleep(1)

    async def get(self, resource: str):
        if not self.started_server:
            self._start_server()
        return requests.get('http://127.0.0.1:8000' + resource).json()

    async def set(self, resource: str, data):
        if not self.started_server:
            self._start_server()

        requests.put(
            url='http://127.0.0.1:8000' + resource,
            json=data
        )

    async def delete(self, resource: str) -> None:
        await self.controller.delete(resource=resource)


def get_test_client():
    if os.environ.get('E2E'):
        return E2ETestClient()

    return UnitTestClient()
