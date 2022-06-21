from abc import abstractmethod
from contextlib import AbstractAsyncContextManager

from seizento.domain.expression import Expression
from seizento.path import Path, StringComponent
from seizento.domain.types.type import Type
from seizento.serializers.expression_serializer import parse_expression, serialize_expression
from seizento.serializers.type_serializer import parse_type, serialize_type
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

    async def get_type(self, path: Path) -> Type:
        data_tree = await self._transaction.get_tree(path=path.insert_first(StringComponent('type')))

        return parse_type(data_tree)

    async def set_type(self, path: Path, value: Type) -> None:
        await self._transaction.set_tree(
            path=path.insert_first(StringComponent('type')),
            tree=serialize_type(value)
        )

    async def delete_type(self, path: Path) -> None:
        await self._transaction.delete_tree(
            path=path.insert_first(StringComponent('type'),)
        )

    async def get_expression(self, path: Path) -> Expression:
        data_tree = await self._transaction.get_tree(path=path.insert_first(StringComponent('expression')))

        return parse_expression(data_tree)

    async def set_expression(self, path: Path, value: Expression) -> None:
        await self._transaction.set_tree(
            path=path.insert_first(StringComponent('expression')),
            tree=serialize_expression(value)
        )
