from typing import Dict

from seizento.controllers.exceptions import NotFound, Forbidden, BadRequest
from seizento.expression.path_service import PathService
from seizento.schema.schema import Schema

from seizento.path import Path
from seizento.repository import Repository
from seizento.serializers.constraint_serializer import parse_constraint, serialize_constraint


class SchemaController:
    def __init__(
        self,
        repository: Repository,
        path: Path
    ):
        self._repository = repository
        self._path = path

    async def _get_target_type(self) -> Schema:
        result = await self._repository.get_schema(path=self._path)
        if result is None:
            raise NotFound

        return result

    async def _get_parent_type(self) -> Schema:
        result = await self._repository.get_schema(path=self._path.remove_last())
        if result is None:
            raise NotFound

        return result

    async def get(self) -> Dict:
        target_type = await self._get_target_type()

        return serialize_constraint(target_type)

    async def set(self, data: Dict) -> None:
        if not self._path.empty:
            parent_type = await self._get_parent_type()

            if parent_type is None:
                raise Forbidden

        try:
            new_schema = parse_constraint(data)
        except Exception as e:
            raise BadRequest from e

        if not isinstance(new_schema, Schema):
            raise BadRequest

        expression = await self._repository.get_expression(path=self._path)

        if expression is not None:
            current_schema = await expression.get_schema(PathService(self._repository))

            if not current_schema.satisfies(new_schema):
                raise Forbidden

        await self._repository.set_schema(
            path=self._path,
            value=new_schema
        )

    async def delete(self) -> None:
        if not self._path.empty:
            parent_type = await self._get_parent_type()

            if parent_type is None:
                raise Forbidden

        await self._repository.delete_type(path=self._path)
