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


class PathEvaluator:
    def __init__(self, repository: Repository):
        self._repository = repository

    async def evaluate(
        self,
        path: Path,
        visited: Set[Path] = None
    ) -> Any:
        visited = visited or set()

        if path in visited:
            raise CircularReference

        nearest_expression = await find_nearest_expression(repository=self._repository, path=path)

        if nearest_expression is None:
            raise NotFound

        indices = [component.name for component in path.components[len(nearest_expression.path):]]

        expression = nearest_expression.expression

        references = expression.get_path_references()

        values = {}
        not_found = False
        for reference in references:
            try:
                values[reference] = await self.evaluate(
                    path=reference,
                    visited=visited | {path}
                )
            except NotFound:
                not_found = True

        if not_found:
            raise NotFound

        evaluation = (await expression.evaluate(evaluator=self, arguments=frozenset()))[frozenset()]

        for index in indices:
            try:
                evaluation = evaluation[index]
            except KeyError:
                raise NotFound

        return evaluation
