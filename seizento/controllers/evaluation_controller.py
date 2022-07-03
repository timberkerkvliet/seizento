from typing import Dict

from seizento.path import Path
from seizento.repository import Repository
from seizento.service.expression_service import PathService


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
