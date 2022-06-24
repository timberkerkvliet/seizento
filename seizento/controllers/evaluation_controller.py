from typing import Dict

from seizento.controllers.exceptions import NotFound
from seizento.controllers.expression_tools import find_nearest_expression
from seizento.path import Path
from seizento.repository import Repository


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

        expression = nearest_expression.expression

        references = expression.get_path_references()
        values = {
            reference: (await self._repository.get_expression(reference)).evaluate({})
            for reference in references
        }

        result = nearest_expression.expression.evaluate(values)

        indices = [component.name for component in self._path.components[len(nearest_expression.path):]]

        for index in indices:
            try:
                result = result[index]
            except Exception:
                raise NotFound

        return result
