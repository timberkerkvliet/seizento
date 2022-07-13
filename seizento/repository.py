from abc import abstractmethod
from contextlib import AbstractAsyncContextManager
from typing import Optional

from seizento.data_tree_maps.constraint_map import constraint_to_tree, tree_to_constraint
from seizento.expression.expression import Expression
from seizento.identifier import Identifier
from seizento.path import Path, LiteralComponent, IndexPlaceHolder, PropertyPlaceHolder
from seizento.schema.constraint import Constraint
from seizento.schema.schema import Schema

from seizento.data_tree_maps.expression_map import tree_to_expression, expression_to_tree
from seizento.data_tree import DataTree
from seizento.serializers.user_serializer import parse_user, serialize_user
from seizento.user import User


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
    def __init__(self, transaction: DataTreeStoreTransaction, root_schema: Constraint):
        self._transaction = transaction
        self._root_schema = root_schema

    async def __aenter__(self):
        await self._transaction.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self._transaction.__aexit__(*args)

    async def get_schema(self, path: Path) -> Optional[Schema]:
        result = self._root_schema.get_children()[LiteralComponent('schema')]
        for component in path:
            if component in result.get_children():
                result = result.get_children()[component]
            elif IndexPlaceHolder() in result.get_children() and isinstance(component, LiteralComponent) and component.value.isdigit():
                result = result.get_children()[IndexPlaceHolder()]
            elif PropertyPlaceHolder() in result.get_children() and isinstance(component, LiteralComponent):
                result = result.get_children()[PropertyPlaceHolder()]
            else:
                raise KeyError

        return result

    async def set_schema(self, path: Path, value: Schema) -> None:
        target = self._root_schema
        for component in path.insert_first(LiteralComponent('schema')).remove_last():
            target = target.get_children()[component]

        target.set_child(
            component=path.last_component if len(path) > 0 else LiteralComponent('schema'),
            constraint=value
        )

    async def delete_type(self, path: Path) -> None:
        target = self._root_schema
        for component in path.insert_first(LiteralComponent('schema')).remove_last():
            target = target.get_children()[component]

        target.delete_child(path.last_component)

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
