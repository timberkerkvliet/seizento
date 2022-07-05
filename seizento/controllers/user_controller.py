from typing import Dict

from seizento.controllers.exceptions import MethodNotAllowed, BadRequest, NotFound
from seizento.identifier import Identifier
from seizento.path import Path, LiteralComponent
from seizento.repository import Repository
from seizento.expression.path_service import PathService
from seizento.serializers.user_serializer import serialize_access_rights, parse_access_rights
from seizento.user import User, HashedPassword


class UserController:
    def __init__(
        self,
        repository: Repository,
        path: Path
    ):
        self._repository = repository
        self._path = path

    def _get_user_id(self) -> Identifier:
        component = self._path.first_component
        return Identifier(component.value)

    async def get(self) -> Dict:
        try:
            user_id = self._get_user_id()
        except Exception as e:
            raise BadRequest from e

        user = await self._repository.get_user(user_id)

        if len(self._path) == 1:
            raise NotFound

        second_component = self._path.remove_first().first_component

        if not isinstance(second_component, LiteralComponent) or second_component.value != 'access_rights':
            raise NotFound

        return serialize_access_rights(user.access_rights)

    async def set(self, data) -> None:
        try:
            user_id = self._get_user_id()
        except Exception as e:
            raise BadRequest from e

        if len(self._path) == 1:
            await self._repository.set_user(
                User(
                    id=user_id,
                    password=HashedPassword.from_password(data['password']),
                    access_rights=parse_access_rights(data['access_rights'])
                )
            )
            return

        user = await self._repository.get_user(user_id)

        await self._repository.set_user(
            user.with_new_password(HashedPassword.from_password(data))
        )

    async def delete(self) -> None:
        raise MethodNotAllowed
