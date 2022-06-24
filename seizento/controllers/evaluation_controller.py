from typing import Dict

from seizento.path import Path
from seizento.repository import Repository
from seizento.service.expression_service import evaluate_expression


class EvaluationController:
    def __init__(
        self,
        repository: Repository,
        path: Path
    ):
        self._repository = repository
        self._path = path

    async def get(self) -> Dict:
        return await evaluate_expression(path=self._path, repository=self._repository)
