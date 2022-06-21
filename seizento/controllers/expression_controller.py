from typing import Dict

from seizento.path import Path
from seizento.repository import Repository
from seizento.serializers.data_tree_serializer import serialize_data_tree, parse_data_tree
from seizento.serializers.type_serializer import parse_type, serialize_type


class ExpressionController:
    def __init__(
        self,
        repository: Repository,
        path: Path
    ):
        self._repository = repository
        self._path = path

    async def _get_target_type(self):
        return await self._repository.get_expression(path=self._path)

    async def get(self) -> Dict:
        target_type = await self._get_target_type()

        return serialize_data_tree(serialize_type(target_type))

    async def set(self, data: Dict) -> None:
        await self._repository.set_expression(
            path=self._path,
            value=parse_expression(parse_data_tree(data))
        )
