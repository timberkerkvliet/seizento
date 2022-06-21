from typing import Dict, Optional

from seizento.controllers.exceptions import NotFound
from seizento.domain.types.type import Type
from seizento.path import Path
from seizento.repository import Repository
from seizento.serializers.data_tree_serializer import serialize_data_tree, parse_data_tree
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
        try:
            return await self._repository.get_type(path=self._path)
        except KeyError as e:
            raise NotFound from e

    async def _get_parent_type(self) -> Optional[Type]:
        if self._path.empty:
            return None
        try:
            return await self._repository.get_type(path=self._path.remove_last())
        except KeyError as e:
            raise NotFound from e

    async def get(self) -> Dict:
        target_type = await self._get_target_type()

        return serialize_data_tree(serialize_type(target_type))

    async def set(self, data: Dict) -> None:
        await self._get_parent_type()
        await self._repository.set_type(
            path=self._path,
            value=parse_type(parse_data_tree(data))
        )

    async def delete(self) -> None:
        await self._repository.delete_type(path=self._path)
