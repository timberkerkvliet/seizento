from typing import Dict

from seizento.controllers.exceptions import NotFound, Forbidden, BadRequest

from seizento.schema.constraint import Constraint
from seizento.schema.schema import Schema

from seizento.path import Path, EMPTY_PATH, LiteralComponent
from seizento.repository import Repository
from seizento.serializers.constraint_serializer import parse_constraint, serialize_constraint


class SchemaController:
    def __init__(
        self,
        repository: Repository,
        path: Path,
        root_schema: Constraint
    ):
        self._repository = repository
        self._path = path
        self._root_schema = root_schema

    def _get_parent_type(self) -> Schema:
        try:
            return self._root_schema.navigate_to(self._path.remove_last())
        except KeyError as e:
            raise NotFound from e

    def get(self) -> Dict:
        try:
            target_type = self._root_schema.navigate_to(self._path)
        except KeyError as e:
            raise NotFound from e

        return serialize_constraint(target_type)

    def set(self, data: Dict) -> None:
        parent_type = self._get_parent_type()

        if parent_type is None:
            raise Forbidden

        try:
            new_schema = parse_constraint(data)
        except Exception as e:
            raise BadRequest from e

        if not isinstance(new_schema, Schema):
            raise BadRequest

        expression = self._repository.get_expression(path=self._path.remove_first())

        if expression is not None:
            current_schema = expression.get_schema(self._repository.get_schema(EMPTY_PATH))

            if not current_schema.satisfies(new_schema):
                raise Forbidden

        try:
            parent_type.set_child(
                component=self._path.last_component,
                constraint=new_schema
            )
        except Exception as e:
            raise NotFound from e

    def delete(self) -> None:
        parent_type = self._get_parent_type()

        if parent_type is None:
            raise Forbidden

        parent_type.delete_child(self._path.last_component)
