from __future__ import annotations

from copy import deepcopy
from typing import Optional, Dict

from seizento.expression.expression import Expression
from seizento.identifier import Identifier
from seizento.path import Path, LiteralComponent
from seizento.schema.constraint import Constraint
from seizento.schema.schema import Schema


from seizento.user import User


class Repository:
    def __init__(self, users: Dict[Identifier, User], root_schema: Constraint, root_expression: Expression):
        self._users = users
        self._root_schema = root_schema
        self._root_expression = root_expression

    def get_expression(self, path: Path) -> Optional[Expression]:
        try:
            result = self._root_expression
        except KeyError:
            return None
        for component in path:
            try:
                result = result.get_child(component)
            except KeyError:
                return None

        return result

    def set_expression(self, path: Path, value: Expression) -> None:
        target = self._root_expression
        for component in path.remove_last():
            target = target.get_child(component)

        target.set_child(
            component=path.last_component,
            expression=value
        )

    def set_expression_temp(self, path: Path, value: Expression) -> Repository:
        repo = Repository(
            root_expression=deepcopy(self._root_expression),
            root_schema=self._root_schema,
            users=self._users
        )
        repo.set_expression(path, value)
        return repo

    def get_user(self, user_id: Identifier) -> Optional[User]:
        if user_id in self._users:
            return self._users[user_id]

        return None

    def set_user(self, user: User) -> None:
        self._users[user.id] = user

    def delete_user(self, user_id: Identifier) -> None:
        self._users.pop(user_id, None)
