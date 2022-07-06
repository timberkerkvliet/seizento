from abc import abstractmethod
from contextlib import AbstractAsyncContextManager
from typing import Optional

from seizento.data_tree_maps.schema_map import schema_to_tree, tree_to_schema
from seizento.expression.expression import Expression
from seizento.identifier import Identifier
from seizento.path import Path, LiteralComponent
from seizento.schema.schema import Schema
from seizento.data_tree_maps.expression_map import tree_to_expression, expression_to_tree
from seizento.data_tree import DataTree
from seizento.serializers.user_serializer import parse_user, serialize_user
from seizento.user import User, AccessRights


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


class Restricted(Exception):
    pass


class RestrictedDataTreeStoreTransaction(DataTreeStoreTransaction):
    def __init__(self, wrapped: DataTreeStoreTransaction, access_rights: AccessRights):
        self._wrapped = wrapped
        self._access_rights = access_rights

    async def __aenter__(self):
        return await self._wrapped.__aenter__()

    async def __aexit__(self, *args):
        return await self._wrapped.__aexit__(*args)

    async def get_tree(self, path: Path) -> DataTree:
        if not self._access_rights.can_read(path):
            raise Restricted

        return await self._wrapped.get_tree(path=path)

    async def set_tree(self, path: Path, tree: DataTree) -> None:
        if not self._access_rights.can_write(path):
            raise Restricted

        return await self._wrapped.set_tree(path=path, tree=tree)

    async def delete_tree(self, path: Path) -> None:
        if not self._access_rights.can_write(path):
            raise Restricted

        return await self._wrapped.delete_tree(path=path)


class Repository:
    def __init__(self, transaction: DataTreeStoreTransaction):
        self._transaction = transaction

    async def __aenter__(self):
        await self._transaction.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self._transaction.__aexit__(*args)

    async def get_schema(self, path: Path) -> Optional[Schema]:
        try:
            data_tree = await self._transaction.get_tree(path=path.insert_first(LiteralComponent('schema')))
        except KeyError:
            return None

        return tree_to_schema(data_tree)

    async def set_schema(self, path: Path, value: Schema) -> None:
        await self._transaction.set_tree(
            path=path.insert_first(LiteralComponent('schema')),
            tree=schema_to_tree(value)
        )

    async def delete_type(self, path: Path) -> None:
        await self._transaction.delete_tree(
            path=path.insert_first(LiteralComponent('schema'), )
        )

    async def get_expression(self, path: Path) -> Optional[Expression]:
        try:
            data_tree = await self._transaction.get_tree(path=path.insert_first(LiteralComponent('expression')))
        except KeyError:
            return None

        return tree_to_expression(data_tree)

    async def set_expression(self, path: Path, value: Expression) -> None:
        await self._transaction.set_tree(
            path=path.insert_first(LiteralComponent('expression')),
            tree=expression_to_tree(value)
        )

    async def get_user(self, user_id: Identifier) -> Optional[User]:
        try:
            data_tree = await self._transaction.get_tree(
                path=Path(components=(LiteralComponent('user'), LiteralComponent(str(user_id))))
            )
        except KeyError:
            return None

        return parse_user(data_tree.root_data)

    async def set_user(self, user: User) -> None:
        await self._transaction.set_tree(
            path=Path(components=(LiteralComponent('user'), LiteralComponent(str(user.id)))),
            tree=DataTree(root_data=serialize_user(user))
        )

    async def delete_user(self, user_id: Identifier) -> None:
        await self._transaction.delete_tree(
            path=Path(components=(LiteralComponent('user'), LiteralComponent(str(user_id)))),
        )
