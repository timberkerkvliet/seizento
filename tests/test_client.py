import uuid

from seizento.controllers.resource_controller import ResourceController
from seizento.domain.expression import Expression
from seizento.domain.path import Path
from seizento.domain.types.type import Type

from seizento.repository import Repository
from seizento.serializers.path_serializer import serialize_component
from seizento.serializers.type_serializer import serialize_root_of_type, parse_type


class FakeRepository(Repository):
    def __init__(self):
        self._types = {}
        self._expressions = {}

    def get_serialized(self, path: Path):
        sub_paths = [
            x for x in self._types.keys()
            if len(x) == len(path) + 1 and x.remove_last_component() == path
        ]

        if not sub_paths:
            return self._types[path]

        return {
            **self._types[path],
            'subtypes': {
                serialize_component(sub_path.last_component): self.get_serialized(sub_path)
                for sub_path in sub_paths
            }
        }

    async def get_type(self, path: Path) -> Type:
        return parse_type(self.get_serialized(path=path))

    async def set_type(self, path: Path, value: Type) -> None:
        self._types[path] = serialize_root_of_type(value)

        sub_paths = [
            x for x in self._types.keys()
            if len(x) == len(path) + 1 and x.remove_last_component() == path
        ]

        for sub_path in sub_paths:
            del self._types[sub_path]

        subtypes = value.get_subtypes()
        if subtypes is None:
            return
        for component, subtype in subtypes.items():
            await self.set_type(path=path.add_component(component), value=subtype)

    async def get_expression(self, path: Path) -> Expression:
        pass

    async def set_expression(self, path: Path, value: Expression) -> None:
        pass


class UnitTestClient:
    ADMIN_TOKEN = 'admin'

    def __init__(self):
        self.controller = ResourceController(
            repository=FakeRepository(),
            user_id=uuid.uuid4()
        )

    async def get(self, resource: str):
        return await self.controller.get(resource=resource)

    async def set(self, resource: str, data):
        await self.controller.set(resource=resource, data=data)

    async def delete(self, resource: str) -> None:
        await self.controller.delete(resource=resource)
