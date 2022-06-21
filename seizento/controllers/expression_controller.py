from typing import Dict

from seizento.path import Path
from seizento.repository import Repository
from seizento.serializers.data_tree_serializer import serialize_data_tree, parse_data_tree
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

        return serialize_data_tree(serialize_expression(expression))

    async def set(self, data: Dict) -> None:
        new_expression = parse_expression(parse_data_tree(data))

        current_type = await self._repository.get_type(path=self._path)
        expression_type = new_expression.get_type()

        if current_type != expression_type:
            raise Exception

        await self._repository.set_expression(
            path=self._path,
            value=new_expression
        )
