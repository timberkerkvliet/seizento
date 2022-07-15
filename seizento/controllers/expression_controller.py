from typing import Dict

from seizento.controllers.exceptions import Forbidden, NotFound, BadRequest

from seizento.path import Path, EMPTY_PATH
from seizento.repository import Repository
from seizento.resource import Root
from seizento.serializers.expression_serializer import serialize_expression, parse_expression
from seizento.expression.path_evaluation import evaluate_expression_at_path


class ExpressionController:
    def __init__(
        self,
        repository: Repository,
        path: Path,
        root: Root
    ):
        self._repository = repository
        self._path = path
        self._root = root

    def _get_expression(self):
        return self._repository.get_expression(path=self._path)

    def get(self) -> Dict:
        expression = self._get_expression()

        if expression is None:
            raise NotFound

        return serialize_expression(expression)

    def set(self, data: Dict) -> None:
        try:
            new_expression = parse_expression(data)
        except Exception as e:
            raise BadRequest from e

        current_type = self._repository.get_schema(path=self._path)
        if current_type is None:
            raise NotFound

        try:
            expression_type = new_expression.get_schema(self._repository.get_schema(EMPTY_PATH))
        except ValueError as e:
            raise Forbidden from e

        if not expression_type.satisfies(current_type):
            raise Forbidden

        if not self._path.empty:
            parent_expression = self._repository.get_expression(path=self._path.remove_last())
            if parent_expression is None:
                raise NotFound

            try:
                parent_expression.set_child(component=self._path.last_component, expression=new_expression)
            except ValueError as e:
                raise Forbidden from e

        repo = self._repository.set_expression_temp(path=self._path, value=new_expression)

        root_expression = repo.get_expression(EMPTY_PATH)

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

        self._repository.set_expression(path=self._path, value=new_expression)
