from dataclasses import dataclass
from typing import Set

from seizento.controllers.exceptions import NotFound
from seizento.expression.expression import Expression
from seizento.path import Path, EMPTY_PATH


@dataclass
class NearestExpressionResult:
    expression: Expression
    path: Path


class CircularReference(Exception):
    pass


class PathService:
    def __init__(self, root_expression: Expression, visited: Set[Path] = None):
        self._root_expression = root_expression
        self._visited = visited or set()

    async def find_nearest_expression(self, path: Path) -> NearestExpressionResult:
        current_path = EMPTY_PATH
        expression = self._root_expression
        for component in path:
            try:
                expression = expression.get_child(component)
            except KeyError:
                break

            current_path = current_path.append(component)

        return NearestExpressionResult(
            expression=expression,
            path=current_path
        )

    async def evaluate(self, path: Path):
        nearest_expression = await self.find_nearest_expression(path=path)

        indices = [
            int(component.value) if component.value.isdigit() else component.value
            for component in path.components[len(nearest_expression.path):]
        ]
        expression = nearest_expression.expression

        evaluation = await expression.evaluate(root_expression=self._root_expression, arguments={})

        for index in indices:
            try:
                evaluation = evaluation[index]
            except (KeyError, IndexError):
                raise NotFound

        return evaluation
