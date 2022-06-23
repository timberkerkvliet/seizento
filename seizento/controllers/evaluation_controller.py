from typing import Dict

from seizento.controllers.exceptions import NotFound
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
        path = self._path
        indices = []
        while True:
            expression = await self._repository.get_expression(self._path)
            if expression is not None:
                break
            else:
                if path.empty:
                    raise NotFound
                indices.append(path.last_component.value)
                path = path.remove_last()
                continue

        result = expression.evaluate()

        for index in indices:
            try:
                result = result[index]
            except Exception:
                raise NotFound

        return result
