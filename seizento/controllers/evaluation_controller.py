from typing import Dict, Any

from seizento.controllers.exceptions import NotFound
from seizento.controllers.expression_tools import find_nearest_expression
from seizento.domain.expression import Expression
from seizento.path import Path
from seizento.repository import Repository


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
        except Exception:
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
