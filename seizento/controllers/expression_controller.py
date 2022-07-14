from typing import Dict

from seizento.controllers.exceptions import Forbidden, NotFound, BadRequest

from seizento.path import Path, EMPTY_PATH
from seizento.repository import Repository
from seizento.serializers.expression_serializer import serialize_expression, parse_expression
from seizento.expression.path_evaluation import evaluate_expression_at_path


class ExpressionController:
    def __init__(
        self,
        repository: Repository,
        path: Path
    ):
        self._repository = repository
        self._path = path

    async def _get_expression(self):
        return await self._repository.get_expression(path=self._path)

    async def get(self) -> Dict:
        expression = await self._get_expression()

        if expression is None:
            raise NotFound

        return serialize_expression(expression)

    async def set(self, data: Dict) -> None:
        try:
            new_expression = parse_expression(data)
        except Exception as e:
            raise BadRequest from e

        current_type = await self._repository.get_schema(path=self._path)
        if current_type is None:
            raise NotFound

        try:
            expression_type = new_expression.get_schema(await self._repository.get_schema(EMPTY_PATH))
        except ValueError as e:
            raise Forbidden from e

        if not expression_type.satisfies(current_type):
            raise Forbidden

        if not self._path.empty:
            parent_expression = await self._repository.get_expression(path=self._path.remove_last())
            if parent_expression is None:
                raise NotFound

            try:
                parent_expression.set_child(component=self._path.last_component, expression=new_expression)
            except ValueError as e:
                raise Forbidden from e

        repo = await self._repository.set_expression_temp(path=self._path, value=new_expression)

        root_expression = await repo.get_expression(EMPTY_PATH)

        path = self._path
        while True:
            try:
                evaluate_expression_at_path(path=path, root_expression=root_expression)
                break
            except RecursionError as e:
                raise Forbidden from e
            except KeyError:
                path = path.remove_last()
                continue

        await self._repository.set_expression(path=self._path, value=new_expression)
