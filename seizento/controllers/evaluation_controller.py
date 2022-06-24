from typing import Dict, Any

from seizento.controllers.exceptions import NotFound
from seizento.controllers.expression_tools import find_nearest_expression
from seizento.domain.expression import Expression
from seizento.path import Path
from seizento.repository import Repository


async def evaluate(expression: Expression, repository: Repository) -> Any:
    references = expression.get_path_references()
    values = {
        reference: await evaluate(
            expression=await repository.get_expression(reference),
            repository=repository
        )
        for reference in references
    }

    return expression.evaluate(values)


class EvaluationController:
    def __init__(
        self,
        repository: Repository,
        path: Path
    ):
        self._repository = repository
        self._path = path

    async def get(self) -> Dict:
        nearest_expression = await find_nearest_expression(repository=self._repository, path=self._path)

        if nearest_expression is None:
            raise NotFound

        evaluation = await evaluate(expression=nearest_expression.expression, repository=self._repository)

        indices = [component.name for component in self._path.components[len(nearest_expression.path):]]

        for index in indices:
            try:
                evaluation = evaluation[index]
            except Exception:
                raise NotFound

        return evaluation
