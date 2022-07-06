from typing import Dict, Any, Callable, Awaitable

import jwt

from seizento.controllers.evaluation_controller import EvaluationController
from seizento.controllers.exceptions import BadRequest, Unauthorized
from seizento.controllers.expression_controller import ExpressionController
from seizento.controllers.login_controller import LoginController
from seizento.controllers.schema_controller import SchemaController
from seizento.controllers.user_controller import UserController
from seizento.path import Path
from seizento.repository import Repository, DataTreeStoreTransaction, RestrictedDataTreeStoreTransaction, Restricted
from seizento.serializers.path_serializer import parse_path
from seizento.serializers.user_serializer import parse_access_rights
from seizento.user import AccessRights


class ResourceController:
    def __init__(
        self,
        transaction_factory: Callable[[], DataTreeStoreTransaction],
        app_secret: str
    ):
        self._transaction_factory = transaction_factory
        self._app_secret = app_secret

    @staticmethod
    def _get_controller(resource_path: Path, repository: Repository):
        resource_type = resource_path.first_component.value
        if resource_type == 'schema':
            return SchemaController(
                repository=repository,
                path=resource_path.remove_first()
            )
        if resource_type == 'expression':
            return ExpressionController(
                repository=repository,
                path=resource_path.remove_first()
            )
        if resource_type == 'evaluation':
            return EvaluationController(
                repository=repository,
                path=resource_path.remove_first()
            )
        if resource_type == 'user':
            return UserController(
                repository=repository,
                path=resource_path.remove_first()
            )

        raise BadRequest

    def _get_access_rights(self, token: str) -> AccessRights:
        try:
            return parse_access_rights(
                jwt.decode(jwt=token, key=self._app_secret, algorithms='HS256')
            )
        except Exception as e:
            raise Unauthorized

    async def _execute(
        self,
        resource: str,
        token: str,
        action: Callable[[Any],Awaitable],
        authorized: Callable[[AccessRights, Path], bool]
    ):
        access_rights = self._get_access_rights(token)
        try:
            resource_path = parse_path(resource)
        except Exception as e:
            raise BadRequest from e

        if not authorized(access_rights, resource_path):
            raise Unauthorized

        repository = Repository(transaction=self._transaction_factory())

        async with repository:
            controller = self._get_controller(resource_path=resource_path, repository=repository)
            return await action(controller)

    async def get(self, resource: str, token: str) -> Dict:
        return await self._execute(
            resource=resource,
            token=token,
            action=lambda controller: controller.get(),
            authorized=lambda access_rights, path: access_rights.can_read(path)
        )

    async def set(self, resource: str, data: Any, token: str) -> None:
        return await self._execute(
            resource=resource,
            token=token,
            action=lambda controller: controller.set(data),
            authorized=lambda access_rights, path: access_rights.can_write(path)
        )

    async def delete(self, resource: str, token: str) -> None:
        return await self._execute(
            resource=resource,
            token=token,
            action=lambda controller: controller.delete(),
            authorized=lambda access_rights, path: access_rights.can_write(path)
        )
