from typing import Dict, Any, Callable
from uuid import UUID

from seizento.controllers.expression_controller import ExpressionController
from seizento.controllers.type_controller import TypeController
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
        resource_path = parse_path(resource)
        resource_type = resource_path.first_component.value
        if resource_type == 'type':
            return TypeController(
                repository=repository,
                path=resource_path.remove_first()
            )
        if resource_type == 'expression':
            return ExpressionController(
                repository=repository,
                path=resource_path.remove_first()
            )

    async def get(self, resource: str) -> Dict:
        async with self._repository_factory() as repository:
            controller = self._get_controller(resource=resource, repository=repository)

            return await controller.get()

    async def set(self, resource: str, data: Any) -> None:
        async with self._repository_factory() as repository:
            controller = self._get_controller(resource=resource, repository=repository)

            await controller.set(data=data)

    async def delete(self, resource: str) -> None:
        raise NotImplementedError
