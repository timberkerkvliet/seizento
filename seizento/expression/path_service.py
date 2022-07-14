from dataclasses import dataclass
from typing import Dict, Any, Optional, Set

from seizento.controllers.exceptions import NotFound
from seizento.expression.expression import Expression, ArgumentSpace
from seizento.path import Path
from seizento.repository import Repository
from seizento.schema.schema import Schema


@dataclass
class NearestExpressionResult:
    expression: Expression
    path: Path


class CircularReference(Exception):
    pass


class PathService:
    def __init__(self, repository: Repository, visited: Set[Path] = None):
        self._repository = repository
        self._visited = visited or set()

    async def find_nearest_expression(self, path: Path) -> NearestExpressionResult:
        current_path = path
        while True:
            expression = await self._repository.get_expression(current_path)
            if expression is not None:
                return NearestExpressionResult(
                    expression=expression,
                    path=current_path
                )

            if path.empty:
                raise NotFound

            path = path.remove_last()
            continue

    async def get_argument_space(self, path: Path) -> ArgumentSpace:
        nearest_expression = await self.find_nearest_expression(path=path)

        return await nearest_expression.expression.get_argument_space(path_service=self)

    async def evaluate(self, path: Path):
        if path in self._visited:
            raise CircularReference

        nearest_expression = await self.find_nearest_expression(path=path)

        indices = [component.name for component in path.components[len(nearest_expression.path):]]
        expression = nearest_expression.expression

        evaluation = await expression.evaluate(
            path_service=PathService(repository=self._repository, visited=self._visited | {path}),
            arguments={}
        )

        for index in indices:
            try:
                evaluation = evaluation[index]
            except KeyError:
                raise NotFound

        return evaluation
