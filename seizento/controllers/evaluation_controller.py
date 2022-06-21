from typing import Dict

from seizento.path import Path
from seizento.repository import Repository


class EvaluationController:
    def __init__(
        self,
        repository: Repository,
        path: Path
    ):
        self._repository = repository
        self._path = path

    async def get(self) -> Dict:
        try:
            expression = await self._repository.get_expression(self._path)
            return expression.evaluate()
        except KeyError:
            pass

        target_type = await self._repository.get_type(self._path)

        return target_type.default_value
