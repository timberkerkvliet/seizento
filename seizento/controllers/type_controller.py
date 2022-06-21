from typing import Dict, Optional

from seizento.controllers.exceptions import NotFound, Forbidden, BadRequest
from seizento.domain.types.array import Array
from seizento.domain.types.dictionary import Dictionary
from seizento.domain.types.function import Function
from seizento.domain.types.struct import Struct
from seizento.domain.types.type import Type
from seizento.path import Path, StringComponent, PlaceHolder
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

        return serialize_type(target_type)

    async def set(self, data: Dict) -> None:
        parent_type = await self._get_parent_type()
        if parent_type is not None \
            and isinstance(self._path.last_component, StringComponent) \
                and not isinstance(parent_type, Struct):
            raise Forbidden

        if parent_type is not None \
                and isinstance(self._path.last_component, PlaceHolder) \
                and not isinstance(parent_type, (Array, Dictionary, Function)):
            raise Forbidden

        try:
            parsed = parse_type(data)
        except Exception as e:
            raise BadRequest from e

        await self._repository.set_type(
            path=self._path,
            value=parsed
        )

    async def delete(self) -> None:
        await self._repository.delete_type(path=self._path)
