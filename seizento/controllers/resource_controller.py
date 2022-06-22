from typing import Dict, Any, Callable
from uuid import UUID

from seizento.controllers.evaluation_controller import EvaluationController
from seizento.controllers.exceptions import BadRequest
from seizento.controllers.expression_controller import ExpressionController
from seizento.controllers.schema_controller import SchemaController
from seizento.repository import Repository
from seizento.serializers.path_serializer import parse_path


class ResourceController:
    def __init__(
        self,
        repository_factory: Callable[[], Repository],
        user_id: UUID
    ):
        self._repository_factory = repository_factory
        self._user_id = user_id

    @staticmethod
    def _get_controller(resource: str, repository: Repository):
        try:
            resource_path = parse_path(resource)
        except Exception as e:
            raise BadRequest from e

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

        raise BadRequest

    async def get(self, resource: str) -> Dict:
        async with self._repository_factory() as repository:
            controller = self._get_controller(resource=resource, repository=repository)

            return await controller.get()

    async def set(self, resource: str, data: Any) -> None:
        async with self._repository_factory() as repository:
            controller = self._get_controller(resource=resource, repository=repository)

            await controller.set(data=data)

    async def delete(self, resource: str) -> None:
        async with self._repository_factory() as repository:
            controller = self._get_controller(resource=resource, repository=repository)

            await controller.delete()
