from typing import Callable

from seizento.path import Path
from seizento.data_tree import DataTree
from seizento.repository import DataTreeStoreTransaction


class InMemoryDataTreeStoreTransaction(DataTreeStoreTransaction):
    def __init__(self, tree: DataTree, on_exit: Callable[[DataTree], None]):
        self._tree = tree
        self._on_exit = on_exit

    async def __aenter__(self):
        pass

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_val is None:
            self._on_exit(self._tree)

    async def get_tree(self, path: Path) -> DataTree:
        return self._tree.get_subtree(path=path)

    async def set_tree(self, path: Path, tree: DataTree) -> None:
        self._tree = self._tree.set_subtree(path=path, subtree=tree)

    async def delete_tree(self, path: Path) -> None:
        self._tree = self._tree.delete_subtree(path=path)


class InMemoryDataTreeStore:
    def __init__(self):
        self._tree = DataTree(root_data={})

    def _set_state(self, tree: DataTree) -> None:
        self._tree = tree

    def get_transaction(self) -> InMemoryDataTreeStoreTransaction:
        return InMemoryDataTreeStoreTransaction(
            tree=self._tree,
            on_exit=self._set_state
        )

