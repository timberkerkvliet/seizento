from typing import Dict

from seizento.controllers.exceptions import MethodNotAllowed, NotFound
from seizento.path import Path, EMPTY_PATH
from seizento.repository import Repository
from seizento.expression.path_service import PathService


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
        path_service = PathService(root_expression=root_expression)

        return await path_service.evaluate(path=self._path)

    async def set(self, data) -> None:
        raise MethodNotAllowed

    async def delete(self) -> None:
        raise MethodNotAllowed
