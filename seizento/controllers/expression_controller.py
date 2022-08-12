from typing import Dict

from seizento.controllers.exceptions import Forbidden, NotFound, BadRequest, MethodNotAllowed

from seizento.path import Path, EMPTY_PATH
from seizento.repository import Repository
from seizento.application_data import ApplicationData
from seizento.serializers.expression_serializer import serialize_expression, parse_expression
from seizento.expression.path_evaluation import evaluate_expression_at_path


class ExpressionController:
    def __init__(
        self,
        repository: Repository,
        path: Path,
        root: ApplicationData
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

    def delete(self) -> None:
        raise MethodNotAllowed

    def set(self, data: Dict) -> None:
        if len(self._path) == 0:
            raise Forbidden
        try:
            new_expression = parse_expression(data)
        except Exception as e:
            raise BadRequest from e

        try:
            schema = self._root.schema.navigate_to(path=self._path)
        except KeyError:
            raise NotFound

        try:
            expression_schema = new_expression.get_schema(self._root.schema)
        except ValueError as e:
            raise Forbidden from e

        if not expression_schema.satisfies(schema):
            raise Forbidden

        parent_expression = self._repository.get_expression(path=self._path.remove_last())
        if parent_expression is None:
            raise NotFound

        try:
            current = parent_expression.get_child(self._path.last_component)
        except KeyError:
            current = None

        try:
            parent_expression.set_child(component=self._path.last_component, expression=new_expression)
        except ValueError as e:
            raise Forbidden from e

        try:
            evaluate_expression_at_path(root_expression=self._root.expression, path=EMPTY_PATH)
        except RecursionError as e:
            if current is not None:
                parent_expression.set_child(component=self._path.last_component, expression=current)
            else:
                parent_expression.delete_child(component=self._path.last_component)
            raise Forbidden from e
