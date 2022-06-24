from abc import abstractmethod
from contextlib import AbstractAsyncContextManager
from typing import Optional

from seizento.data_tree_maps.schema_map import schema_to_tree, tree_to_schema
from seizento.expression.expression import Expression
from seizento.path import Path, StringComponent
from seizento.domain.schema.schema import Schema
from seizento.data_tree_maps.expression_map import tree_to_expression, expression_to_tree
from seizento.data_tree import DataTree


class DataTreeStoreTransaction(AbstractAsyncContextManager):
    @abstractmethod
    async def get_tree(self, path: Path) -> DataTree:
        ...

    @abstractmethod
    async def set_tree(self, path: Path, tree: DataTree) -> None:
        ...

    @abstractmethod
    async def delete_tree(self, path: Path) -> None:
        ...


class Repository:
    def __init__(self, transaction: DataTreeStoreTransaction):
        self._transaction = transaction

    async def __aenter__(self):
        await self._transaction.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self._transaction.__aexit__(*args)

    async def get_type(self, path: Path) -> Optional[Schema]:
        try:
            data_tree = await self._transaction.get_tree(path=path.insert_first(StringComponent('type')))
        except KeyError:
            return None

        return tree_to_schema(data_tree)

    async def set_type(self, path: Path, value: Schema) -> None:
        await self._transaction.set_tree(
            path=path.insert_first(StringComponent('type')),
            tree=schema_to_tree(value)
        )

    async def delete_type(self, path: Path) -> None:
        await self._transaction.delete_tree(
            path=path.insert_first(StringComponent('type'),)
        )

    async def get_expression(self, path: Path) -> Optional[Expression]:
        try:
            data_tree = await self._transaction.get_tree(path=path.insert_first(StringComponent('expression')))
        except KeyError:
            return None

        return tree_to_expression(data_tree)

    async def set_expression(self, path: Path, value: Expression) -> None:
        await self._transaction.set_tree(
            path=path.insert_first(StringComponent('expression')),
            tree=expression_to_tree(value)
        )
