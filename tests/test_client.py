import uuid

from seizento.controllers.resource_controller import ResourceController
from seizento.path import Path
from seizento.data_tree import DataTree
from seizento.repository import Repository, DataTreeStoreTransaction


class FakeDataTreeStoreTransaction(DataTreeStoreTransaction):
    def __init__(self):
        self._tree = DataTree(values={})

    async def __aenter__(self):
        pass

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def get_tree(self, path: Path) -> DataTree:
        return self._tree.get_subtree(path=path)

    async def set_tree(self, path: Path, tree: DataTree) -> None:
        self._tree = self._tree.set_subtree(path=path, subtree=tree)

    async def delete_tree(self, path: Path) -> None:
        self._tree = self._tree.delete_subtree(path=path)


class UnitTestClient:
    ADMIN_TOKEN = 'admin'

    def __init__(self):
        self.controller = ResourceController(
            repository_factory=lambda: Repository(FakeDataTreeStoreTransaction()),
            user_id=uuid.uuid4()
        )

    async def get(self, resource: str):
        return await self.controller.get(resource=resource)

    async def set(self, resource: str, data):
        await self.controller.set(resource=resource, data=data)

    async def delete(self, resource: str) -> None:
        await self.controller.delete(resource=resource)
