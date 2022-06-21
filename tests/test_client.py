import uuid

from seizento.controllers.resource_controller import ResourceController
from seizento.path import Path
from seizento.data_tree import PathValueStoreTransaction, DataTree
from seizento.repository import Repository


class FakePathyValueStoreTransaction(PathValueStoreTransaction):
    def __init__(self):
        self._root_values = DataTree(values={})

    async def get_tree(self, path: Path) -> DataTree:
        pass

    async def set_tree(self, path: Path, values: DataTree) -> None:
        pass

    async def delete_tree(self, path: Path) -> None:
        pass


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
