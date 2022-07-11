from typing import Dict

from seizento.controllers.exceptions import Forbidden, NotFound, BadRequest

from seizento.path import Path
from seizento.repository import Repository
from seizento.serializers.expression_serializer import serialize_expression, parse_expression
from seizento.expression.path_service import CircularReference, PathService


class ExpressionController:
    def __init__(
        self,
        repository: Repository,
        path: Path
    ):
        self._repository = repository
        self._path = path

    async def _get_expression(self):
        return await self._repository.get_expression(path=self._path)

    async def get(self) -> Dict:
        expression = await self._get_expression()

        if expression is None:
            raise NotFound

        return serialize_expression(expression)

    async def set(self, data: Dict) -> None:
        try:
            new_expression = parse_expression(data)
        except Exception as e:
            raise BadRequest from e

        current_type = await self._repository.get_schema(path=self._path)
        if current_type is None:
            raise KeyError

        try:
            expression_type = await new_expression.get_schema(PathService(self._repository))
        except ValueError as e:
            raise Forbidden from e

        if not expression_type.conforms_to(current_type):
            raise Forbidden

        if not self._path.empty:
            parent_expression = await self._repository.get_expression(path=self._path.remove_last())
            if parent_expression is None:
                raise NotFound

            if not parent_expression.supports_child_at(self._path.last_component):
                raise Forbidden

        await self._repository.set_expression(path=self._path, value=new_expression)

        path_service = PathService(repository=self._repository)

        path = self._path
        while True:
            try:
                await path_service.evaluate(path=path)
                return
            except CircularReference as e:
                raise Forbidden from e
            except NotFound:
                return
            except KeyError:
                path = path.remove_last()
                continue
