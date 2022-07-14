from typing import Dict, Callable
from uuid import UUID

import jwt

from seizento.controllers.exceptions import MethodNotAllowed, Unauthorized
from seizento.expression.expression import Expression
from seizento.identifier import Identifier
from seizento.path import Path
from seizento.repository import Repository, DataTreeStoreTransaction
from seizento.expression.path_service import PathService
from seizento.schema.constraint import Constraint
from seizento.serializers.user_serializer import serialize_access_rights
from seizento.user import User


class LoginController:
    def __init__(
        self,
        users: Dict[Identifier, User],
        app_secret: str,
        root_schema: Constraint,
        root_expression: Expression
    ):
        self._users = users
        self._app_secret = app_secret
        self._root_schema = root_schema
        self._root_expression = root_expression

    async def login(self, data) -> str:
        repository = Repository(
            users=self._users,
            root_schema=self._root_schema,
            root_expression=self._root_expression
        )

        user = await repository.get_user(Identifier(data['user_id']))

        if user is None or not user.password.check_password(data['password']):
            raise Unauthorized

        return jwt.encode(
            payload=serialize_access_rights(user.access_rights),
            key=self._app_secret
        )
