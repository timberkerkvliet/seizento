from dataclasses import dataclass
from typing import Dict, Any, Optional

from seizento.controllers.exceptions import NotFound
from seizento.expression.expression import Expression
from seizento.path import Path
from seizento.repository import Repository


@dataclass(frozen=True)
class NearestExpressionResult:
    expression: Expression
    path: Path


async def find_nearest_expression(repository: Repository, path: Path) -> Optional[NearestExpressionResult]:
    current_path = path
    while True:
        expression = await repository.get_expression(current_path)
        if expression is not None:
            return NearestExpressionResult(
                expression=expression,
                path=current_path
            )

        if path.empty:
            return None

        path = path.remove_last()
        continue


async def evaluate(path: Path, repository: Repository) -> Any:
    nearest_expression = await find_nearest_expression(repository=repository, path=path)

    if nearest_expression is None:
        raise NotFound

    references = nearest_expression.expression.get_path_references()
    values = {
        reference: await evaluate(
            path=reference,
            repository=repository
        ) for reference in references
    }

    evaluation = nearest_expression.expression.evaluate(values)

    indices = [component.name for component in path.components[len(nearest_expression.path):]]

    for index in indices:
        try:
            evaluation = evaluation[index]
        except KeyError:
            raise NotFound

    return evaluation


class EvaluationController:
    def __init__(
        self,
        repository: Repository,
        path: Path
    ):
        self._repository = repository
        self._path = path

    async def get(self) -> Dict:
        return await evaluate(path=self._path, repository=self._repository)
