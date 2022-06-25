import uuid
from typing import Callable

from seizento.controllers.resource_controller import ResourceController
from seizento.path import Path, EMPTY_PATH, StringComponent
from seizento.data_tree import DataTree
from seizento.repository import Repository, DataTreeStoreTransaction


class FakeDataTreeStoreTransaction(DataTreeStoreTransaction):
    def __init__(self, tree: DataTree, on_exit: Callable[[DataTree], None]):
        self._tree = tree
        self._on_exit = on_exit

    async def __aenter__(self):
        pass

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self._on_exit(self._tree)

    async def get_tree(self, path: Path) -> DataTree:
        return self._tree.get_subtree(path=path)

    async def set_tree(self, path: Path, tree: DataTree) -> None:
        self._tree = self._tree.set_subtree(path=path, subtree=tree)

    async def delete_tree(self, path: Path) -> None:
        self._tree = self._tree.delete_subtree(path=path)


class FakeDataTreeStore:
    def __init__(self):
        self._tree = DataTree(values={EMPTY_PATH: {}})

    def _set_state(self, tree: DataTree) -> None:
        self._tree = tree

    def get_transaction(self) -> FakeDataTreeStoreTransaction:
        return FakeDataTreeStoreTransaction(
            tree=self._tree,
            on_exit=self._set_state
        )


class UnitTestClient:
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
