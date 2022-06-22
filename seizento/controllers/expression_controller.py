from typing import Dict

from seizento.controllers.exceptions import Forbidden
from seizento.path import Path
from seizento.repository import Repository
from seizento.serializers.expression_serializer import serialize_expression, parse_expression


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

        return serialize_expression(expression)

    async def set(self, data: Dict) -> None:
        new_expression = parse_expression(data)

        current_type = await self._repository.get_type(path=self._path)
        expression_type = new_expression.get_type()

        if not expression_type.is_subschema(current_type):
            raise Forbidden

        await self._repository.set_expression(
            path=self._path,
            value=new_expression
        )
