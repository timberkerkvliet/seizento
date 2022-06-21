from typing import Dict, Any, List, Callable
from uuid import UUID

from seizento.controllers.type_controller import TypeController
from seizento.repository import Repository
from seizento.serializers.path_serializer import parse_path


def parse_resource(value: str) -> List[str]:
    parts = value.split('/')

    return [part for part in parts if len(part) > 0]


class ResourceController:
    def __init__(
        self,
        repository_factory: Callable[[], Repository],
        user_id: UUID
    ):
        self._repository_factory = repository_factory
        self._user_id = user_id

    async def get(self, resource: str) -> Dict:
        async with self._repository_factory() as repository:
            resource_path = parse_path(resource)
            resource_type = resource_path.first_component.value

            if resource_type == 'type':
                controller = TypeController(
                    repository=repository,
                    path=resource_path.remove_first()
                )
                return await controller.get()

            raise NotImplementedError

    async def set(self, resource: str, data: Any) -> None:
        async with self._repository_factory() as repository:
            resource_path = parse_path(resource)
            resource_type = resource_path.first_component.value

            if resource_type == 'type':
                controller = TypeController(
                    repository=repository,
                    path=resource_path.remove_first()
                )
                return await controller.set(data=data)

    async def delete(self, resource: str) -> None:
        raise NotImplementedError



