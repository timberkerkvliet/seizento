from typing import Dict, Callable
from uuid import UUID

import jwt

from seizento.controllers.exceptions import MethodNotAllowed, Unauthorized
from seizento.identifier import Identifier
from seizento.path import Path
from seizento.repository import Repository, DataTreeStoreTransaction
from seizento.expression.path_service import PathService
from seizento.serializers.user_serializer import serialize_access_rights


class LoginController:
    def __init__(
        self,
        transaction_factory: Callable[[], DataTreeStoreTransaction],
        token_secret: str
    ):
        self._transaction_factory = transaction_factory
        self._token_secret = token_secret

    async def login(self, data) -> str:
        repository = Repository(transaction=self._transaction_factory())

        async with repository:
            user = await repository.get_user(Identifier(data['user_id']))

            if user is None or not user.password.check_password(data['password']):
                raise Unauthorized

            return jwt.encode(
                payload=serialize_access_rights(user.access_rights),
                key=self._token_secret
            )
