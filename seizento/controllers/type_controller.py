from typing import Dict

from seizento.path import Path
from seizento.repository import Repository
from seizento.serializers.type_serializer import parse_type, serialize_type


class TypeController:
    def __init__(
        self,
        repository: Repository,
        path: Path
    ):
        self._repository = repository
        self._path = path

    async def _get_target_type(self):
        return await self._repository.get_type(path=self._path)

    async def get(self) -> Dict:
        target_type = await self._get_target_type()

        return serialize_type(target_type)

    async def set(self, data: Dict) -> None:
        await self._repository.set_type(
            path=self._path,
            value=parse_type(data)
        )
