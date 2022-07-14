from typing import Dict, Any, Callable, Awaitable

import jwt

from seizento.controllers.evaluation_controller import EvaluationController
from seizento.controllers.exceptions import BadRequest, Unauthorized
from seizento.controllers.expression_controller import ExpressionController
from seizento.controllers.schema_controller import SchemaController
from seizento.controllers.user_controller import UserController
from seizento.expression.expression import Expression
from seizento.identifier import Identifier
from seizento.path import Path
from seizento.repository import Repository
from seizento.schema.constraint import Constraint
from seizento.serializers.path_serializer import parse_path
from seizento.serializers.user_serializer import parse_access_rights
from seizento.user import AccessRights, User


class ResourceController:
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

    def _get_controller(self, resource_path: Path, repository: Repository):
        resource_type = resource_path.first_component.value
        if resource_type == 'schema':
            return SchemaController(
                repository=repository,
                path=resource_path.remove_first(),
                root_schema=self._root_schema
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

    @staticmethod
    def _get_resource_path(resource: str) -> Path:
        try:
            return parse_path(resource)
        except Exception as e:
            raise BadRequest from e

    async def get(self, resource: str, token: str) -> Dict:
        access_rights = self._get_access_rights(token)
        resource_path = self._get_resource_path(resource)

        if not access_rights.can_read(resource_path):
            raise Unauthorized

        repository = Repository(
            users=self._users,
            root_schema=self._root_schema,
            root_expression=self._root_expression
        )

        controller = self._get_controller(resource_path=resource_path, repository=repository)
        return await controller.get()

    async def set(self, resource: str, data: Any, token: str) -> None:
        access_rights = self._get_access_rights(token)
        resource_path = self._get_resource_path(resource)

        if not access_rights.can_write(resource_path):
            raise Unauthorized

        repository = Repository(
            users=self._users,
            root_schema=self._root_schema,
            root_expression=self._root_expression
        )

        controller = self._get_controller(resource_path=resource_path, repository=repository)
        await controller.set(data)

    async def delete(self, resource: str, token: str) -> None:
        access_rights = self._get_access_rights(token)
        resource_path = self._get_resource_path(resource)

        if not access_rights.can_write(resource_path):
            raise Unauthorized

        repository = Repository(
            users=self._users,
            root_schema=self._root_schema,
            root_expression=self._root_expression
        )

        controller = self._get_controller(resource_path=resource_path, repository=repository)
        await controller.delete()
