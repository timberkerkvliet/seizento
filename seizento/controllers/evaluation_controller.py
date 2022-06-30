from typing import Dict

from seizento.path import Path
from seizento.repository import Repository
from seizento.service.expression_service import ExpressionEvaluator


class EvaluationController:
    def __init__(
        self,
        repository: Repository,
        path: Path
    ):
        self._repository = repository
        self._path = path

    async def get(self) -> Dict:
        evaluator = ExpressionEvaluator(repository=self._repository)

        return await evaluator.evaluate(path=self._path)
