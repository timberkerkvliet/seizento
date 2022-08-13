from typing import Dict

from seizento.application_data import ApplicationData
from seizento.controllers.exceptions import BadRequest, NotFound, Forbidden
from seizento.identifier import Identifier
from seizento.path import Path, LiteralComponent
from seizento.serializers.user_serializer import serialize_access_rights, parse_access_rights
from seizento.user import User, HashedPassword, ADMIN_USER


class UserController:
    def __init__(
        self,
        path: Path,
        root: ApplicationData
    ):
        self._path = path
        self._root = root

    def _get_user_id(self) -> Identifier:
        component = self._path.first_component
        return Identifier(component.value)

    def get(self) -> Dict:
        try:
            user_id = self._get_user_id()
        except Exception as e:
            raise BadRequest from e

        user = self._root.users.get(user_id)

        if len(self._path) == 1:
            raise NotFound

        second_component = self._path.remove_first().first_component

        if not isinstance(second_component, LiteralComponent) or second_component.value != 'access_rights':
            raise NotFound

        return serialize_access_rights(user.access_rights)

    def set(self, data) -> None:
        try:
            user_id = self._get_user_id()
        except Exception as e:
            raise BadRequest from e

        if len(self._path) == 1:
            self._root.users[user_id] = \
                User(
                    id=user_id,
                    hashed_password=HashedPassword.from_password(data['password']),
                    access_rights=parse_access_rights(data['access_rights'])
                )

            return

        user = self._root.users.get(user_id)

        self._root.users[user_id] = user.with_new_password(HashedPassword.from_password(data))

    def delete(self) -> None:
        try:
            user_id = self._get_user_id()
        except Exception as e:
            raise BadRequest from e

        if user_id == ADMIN_USER.id:
            raise Forbidden

        if len(self._path) > 1:
            raise BadRequest

        del self._root.users[user_id]
