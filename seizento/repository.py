from __future__ import annotations

from copy import deepcopy
from typing import Optional, Dict

from seizento.application_data import ApplicationData
from seizento.expression.expression import Expression
from seizento.identifier import Identifier
from seizento.path import Path, LiteralComponent
from seizento.schema.constraint import Constraint
from seizento.schema.schema import Schema


from seizento.user import User


class Repository:
    def __init__(self, application_data: ApplicationData):
        self._data = application_data

    def get_expression(self, path: Path) -> Optional[Expression]:
        try:
            result = self._data.expression
        except KeyError:
            return None
        for component in path:
            try:
                result = result.get_child(component)
            except KeyError:
                return None

        return result

    def set_expression(self, path: Path, value: Expression) -> None:
        target = self._data.expression
        for component in path.remove_last():
            target = target.get_child(component)

        target.set_child(
            component=path.last_component,
            expression=value
        )

    def get_user(self, user_id: Identifier) -> Optional[User]:
        if user_id in self._data.users:
            return self._data.users[user_id]

        return None

    def set_user(self, user: User) -> None:
        self._data.users[user.id] = user

    def delete_user(self, user_id: Identifier) -> None:
        self._data.users.pop(user_id, None)
