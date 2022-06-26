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


async def evaluate_expression_at_path(path: Path, repository: Repository) -> Any:
    nearest_expression = await find_nearest_expression(repository=repository, path=path)

    if nearest_expression is None:
        raise NotFound

    indices = [component.name for component in path.components[len(nearest_expression.path):]]

    evaluation = await evaluate_expression(expression=nearest_expression.expression, repository=repository)

    for index in indices:
        try:
            evaluation = evaluation[index]
        except KeyError:
            raise NotFound

    return evaluation


async def evaluate_expression(expression: Expression, repository: Repository) -> Any:
    references = expression.get_path_references()
    values = {
        reference: await evaluate_expression_at_path(
            path=reference,
            repository=repository
        ) for reference in references
    }

    return expression.evaluate(values)


async def has_circular_dependencies(expression: Expression, repository: Repository) -> bool:
    return False
