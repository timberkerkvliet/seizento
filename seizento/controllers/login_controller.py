from typing import Dict

import jwt

from seizento.controllers.exceptions import Unauthorized, BadRequest
from seizento.identifier import Identifier
from seizento.serializers.user_serializer import serialize_access_rights
from seizento.user import User


class LoginController:
    def __init__(
        self,
        users: Dict[Identifier, User],
        app_secret: str
    ):
        self._users = users
        self._app_secret = app_secret

    async def login(self, data) -> str:
        try:
            user_id = Identifier(data['user_id'])
        except Exception as e:
            raise BadRequest from e

        if user_id not in self._users:
            raise Unauthorized

        user = self._users[user_id]

        if user is None or not user.password.check_password(data['password']):
            raise Unauthorized

        return jwt.encode(
            payload=serialize_access_rights(user.access_rights),
            key=self._app_secret
        )
