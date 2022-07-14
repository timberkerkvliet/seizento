from typing import Dict

from seizento.controllers.exceptions import MethodNotAllowed, NotFound
from seizento.path import Path, EMPTY_PATH
from seizento.repository import Repository
from seizento.expression.path_evaluation import evaluate_expression_at_path


class EvaluationController:
    def __init__(
        self,
        repository: Repository,
        path: Path
    ):
        self._repository = repository
        self._path = path

    def get(self) -> Dict:
        root_expression = self._repository.get_expression(EMPTY_PATH)
        if root_expression is None:
            raise NotFound

        return evaluate_expression_at_path(path=self._path, root_expression=root_expression)

    def set(self, data) -> None:
        raise MethodNotAllowed

    def delete(self) -> None:
        raise MethodNotAllowed
