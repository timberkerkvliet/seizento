from typing import Callable
from uuid import UUID

from seizento.path import Path, LiteralComponent, EMPTY_PATH
from seizento.data_tree import DataTree
from seizento.repository import DataTreeStoreTransaction
from seizento.serializers.user_serializer import serialize_user
from seizento.user import User, AccessRights


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
    def __init__(self, admin_user: User):
        self._tree = DataTree(
            root_data={},
            subtrees={
                LiteralComponent('user'): DataTree(
                    root_data={},
                    subtrees={
                        LiteralComponent(str(admin_user.id)): DataTree(root_data=serialize_user(admin_user))
                    }
                )
            }
        )

    def _set_state(self, tree: DataTree) -> None:
        self._tree = tree

    def get_transaction(self) -> InMemoryDataTreeStoreTransaction:
        return InMemoryDataTreeStoreTransaction(
            tree=self._tree,
            on_exit=self._set_state
        )

