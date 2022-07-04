from unittest import IsolatedAsyncioTestCase

from seizento.adapters.sqllite_data_tree_store import SQLiteDataTreeStore
from seizento.data_tree import DataTree
from seizento.path import EMPTY_PATH, LiteralComponent, Path


class TestSQLiteDataTreeStore(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.store = SQLiteDataTreeStore(db_path='test-data.sql')
        transaction = self.store.get_transaction()

        async with transaction:
            await transaction.delete_tree(EMPTY_PATH)

    async def test_get_root(self):
        tree = DataTree(
            root_data={'a': 1},
            subtrees={
                LiteralComponent('hey'): DataTree(root_data={'b': 2})
            }
        )

        async with self.store.get_transaction() as transaction:
            await transaction.set_tree(
                path=EMPTY_PATH,
                tree=tree
            )

        async with self.store.get_transaction() as transaction:
            result = await transaction.get_tree(
                path=EMPTY_PATH
            )

        self.assertEqual(tree, result)

    async def test_add_child(self):
        tree = DataTree(
            root_data={'a': 1},
            subtrees={
                LiteralComponent('hey'): DataTree(root_data={'b': 2})
            }
        )

        async with self.store.get_transaction() as transaction:
            await transaction.set_tree(
                path=EMPTY_PATH,
                tree=tree
            )

        async with self.store.get_transaction() as transaction:
            await transaction.set_tree(
                path=Path(components=(LiteralComponent('hoi'),)),
                tree=DataTree(root_data={'hoi': 'hoi'})
            )

        async with self.store.get_transaction() as transaction:
            result = await transaction.get_tree(
                path=EMPTY_PATH
            )

        self.assertEqual(DataTree(
            root_data={'a': 1},
            subtrees={
                LiteralComponent('hey'): DataTree(root_data={'b': 2}),
                LiteralComponent('hoi'): DataTree(root_data={'hoi': 'hoi'})
            }
        ), result)
