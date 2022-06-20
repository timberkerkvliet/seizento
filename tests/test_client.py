import uuid
from typing import Dict

from seizento.controllers.resource_controller import ResourceController
from seizento.key_value_store import KeyValueStoreTransaction
from seizento.repository import Repository


class FakeKeyValueStoreTransaction(KeyValueStoreTransaction):
    def __init__(self):
        self._values: Dict[str, str] = {}

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        ...

    async def get(self, key: str) -> str:
        return self._values[key]

    async def set(self, key: str, value: str) -> None:
        self._values[key] = value

    async def delete(self, key: str) -> None:
        del self._values[key]

    async def find(self, key_prefix: str) -> Dict[str, str]:
        return {
            key: value for key, value in self._values.items()
            if key.startswith(key_prefix)
        }


class UnitTestClient:
    ADMIN_TOKEN = 'admin'

    def __init__(self):
        self.controller = ResourceController(
            repository=Repository(FakeKeyValueStoreTransaction()),
            user_id=uuid.uuid4()
        )

    async def get(self, resource: str):
        return await self.controller.get(resource=resource)

    async def set(self, resource: str, data):
        await self.controller.set(resource=resource, data=data)

    async def delete(self, resource: str) -> None:
        await self.controller.delete(resource=resource)
