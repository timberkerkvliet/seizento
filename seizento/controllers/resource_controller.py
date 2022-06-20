from typing import Dict, Any, List
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
        repository: Repository,
        user_id: UUID
    ):
        self._repository = repository
        self._user_id = user_id

    async def get(self, resource: str) -> Dict:
        parts = parse_resource(resource)

        if parts[0] == 'type':
            controller = TypeController(
                repository=self._repository,
                path=parse_path('/'.join(parts[1:]))
            )
            return await controller.get()

        raise NotImplementedError

    async def set(self, resource: str, data: Any) -> None:
        parts = parse_resource(resource)

        if parts[0] == 'type':
            controller = TypeController(
                repository=self._repository,
                path=parse_path('/'.join(parts[1:]))
            )
            return await controller.set(data=data)

    async def delete(self, resource: str) -> None:
        raise NotImplementedError



