from typing import Dict

from seizento.controllers.exceptions import Forbidden, NotFound

from seizento.path import Path
from seizento.repository import Repository
from seizento.serializers.expression_serializer import serialize_expression, parse_expression
from seizento.service.expression_service import can_reach_cycles_or_targets, evaluate_expression_at_path, \
    CircularReference


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
        new_expression = parse_expression(data)

        current_type = await self._repository.get_type(path=self._path)
        if current_type is None:
            raise KeyError

        references = new_expression.get_path_references()
        schemas = {
            reference: await self._repository.get_type(reference)
            for reference in references
        }
        expression_type = new_expression.get_schema(schemas)

        if not expression_type.is_subschema(current_type):
            raise Forbidden

        if not self._path.empty:
            parent_expression = await self._repository.get_expression(path=self._path.remove_last())
            if parent_expression is None:
                raise NotFound

            if not parent_expression.supports_child_at(self._path.last_component):
                raise Forbidden

        await self._repository.set_expression(path=self._path, value=new_expression)

        try:
            await evaluate_expression_at_path(path=self._path, repository=self._repository)
        except CircularReference as e:
            raise Forbidden from e
        except NotFound:
            pass
