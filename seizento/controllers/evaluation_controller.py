from typing import Dict

from seizento.path import Path
from seizento.repository import Repository
from seizento.serializers.data_tree_serializer import serialize_data_tree, parse_data_tree
from seizento.serializers.expression_serializer import serialize_expression, parse_expression


class EvaluationController:
    def __init__(
        self,
        repository: Repository,
        path: Path
    ):
        self._repository = repository
        self._path = path

    async def get(self) -> Dict:
        expression = await self._repository.get_expression(self._path)

        return expression.evaluate()
