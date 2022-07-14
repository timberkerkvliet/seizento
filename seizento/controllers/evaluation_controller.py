from typing import Dict

from seizento.controllers.exceptions import MethodNotAllowed, NotFound
from seizento.path import Path, EMPTY_PATH
from seizento.repository import Repository
from seizento.expression.path_service import evaluate_expression_at_path


class EvaluationController:
    def __init__(
        self,
        repository: Repository,
        path: Path
    ):
        self._repository = repository
        self._path = path

    async def get(self) -> Dict:
        root_expression = await self._repository.get_expression(EMPTY_PATH)
        if root_expression is None:
            raise NotFound

        return evaluate_expression_at_path(path=self._path, root_expression=root_expression)

    async def set(self, data) -> None:
        raise MethodNotAllowed

    async def delete(self) -> None:
        raise MethodNotAllowed
