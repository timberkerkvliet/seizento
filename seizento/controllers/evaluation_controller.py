from typing import Dict

from seizento.controllers.exceptions import MethodNotAllowed
from seizento.path import Path
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
        path_service = PathService(repository=self._repository)

        return await path_service.evaluate(path=self._path)

    async def set(self, data) -> None:
        raise MethodNotAllowed

    async def delete(self) -> None:
        raise MethodNotAllowed
