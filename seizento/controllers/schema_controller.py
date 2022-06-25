from typing import Dict

from seizento.controllers.exceptions import NotFound, Forbidden, BadRequest
from seizento.schema.array import Array
from seizento.schema.dictionary import Dictionary

from seizento.schema.struct import Struct
from seizento.schema.schema import Schema
from seizento.path import Path, StringComponent, PlaceHolder
from seizento.repository import Repository
from seizento.serializers.schema_serializer import parse_schema, serialize_schema


class SchemaController:
    def __init__(
        self,
        repository: Repository,
        path: Path
    ):
        self._repository = repository
        self._path = path

    async def _get_target_type(self) -> Schema:
        result = await self._repository.get_type(path=self._path)
        if result is None:
            raise NotFound

        return result

    async def _get_parent_type(self) -> Schema:
        if self._path.empty:
            raise NotFound

        result = await self._repository.get_type(path=self._path.remove_last())
        if result is None:
            raise NotFound

        return result

    async def get(self) -> Dict:
        target_type = await self._get_target_type()

        return serialize_schema(target_type)

    async def set(self, data: Dict) -> None:
        if not self._path.empty:
            parent_type = await self._get_parent_type()

            if not parent_type.supports_child_at(self._path.last_component):
                raise Forbidden

        try:
            new_schema = parse_schema(data)
        except Exception as e:
            raise BadRequest from e

        expression = await self._repository.get_expression(path=self._path)

        if expression is not None:
            references = expression.get_path_references()
            schemas = {
                reference: await self._repository.get_type(reference)
                for reference in references
            }
            if not expression.get_schema(schemas).is_subschema(new_schema):
                raise Forbidden

        await self._repository.set_type(
            path=self._path,
            value=new_schema
        )

    async def delete(self) -> None:
        await self._repository.delete_type(path=self._path)
