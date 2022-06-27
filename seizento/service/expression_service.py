from dataclasses import dataclass
from typing import Dict, Any, Optional, Set

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


class CircularReference(Exception):
    pass


async def evaluate_expression_at_path(
    path: Path,
    repository: Repository,
    visited: Set[Path] = None
) -> Any:
    visited = visited or set()

    if path in visited:
        raise CircularReference

    nearest_expression = await find_nearest_expression(repository=repository, path=path)

    if nearest_expression is None:
        raise NotFound

    indices = [component.name for component in path.components[len(nearest_expression.path):]]

    expression = nearest_expression.expression

    references = expression.get_path_references()

    values = {}
    not_found = False
    for reference in references:
        try:
            values[reference] = await evaluate_expression_at_path(
                path=reference,
                repository=repository,
                visited=visited | {path}
            )
        except NotFound:
            not_found = True

    if not_found:
        raise NotFound

    evaluation = expression.evaluate(values)

    for index in indices:
        try:
            evaluation = evaluation[index]
        except KeyError:
            raise NotFound

    return evaluation
