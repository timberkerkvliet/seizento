from typing import Dict

from seizento.controllers.exceptions import NotFound, Forbidden, BadRequest
from seizento.resource import Root

from seizento.schema.constraint import Constraint
from seizento.schema.schema import Schema

from seizento.path import Path, EMPTY_PATH, LiteralComponent
from seizento.repository import Repository
from seizento.serializers.constraint_serializer import parse_constraint, serialize_constraint


class SchemaController:
    def __init__(self, path: Path, root: Root):
        self._path = path
        self._root = root

    def get(self) -> Dict:
        try:
            target_type = self._root.schema.navigate_to(self._path)
        except KeyError as e:
            raise NotFound from e

        return serialize_constraint(target_type)

    def _get_parent_type(self) -> Schema:
        try:
            return self._root.schema.navigate_to(self._path.remove_last())
        except KeyError as e:
            raise NotFound from e

    def set(self, data: Dict) -> None:
        parent_type = self._get_parent_type()

        if parent_type is None:
            raise Forbidden

        try:
            new_schema = parse_constraint(data)
        except Exception as e:
            raise BadRequest from e

        try:
            current = parent_type.get_child(self._path.last_component)
        except KeyError:
            current = None

        try:
            parent_type.set_child(
                component=self._path.last_component,
                constraint=new_schema
            )
        except Exception as e:
            raise NotFound from e

        if not self._root.expression.get_schema(self._root.schema).satisfies(self._root.schema):
            if current is not None:
                parent_type.set_child(
                    component=self._path.last_component,
                    constraint=current
                )
            else:
                parent_type.delete_child(self._path.last_component)

            raise Forbidden

    def delete(self) -> None:
        parent_type = self._get_parent_type()

        if parent_type is None:
            raise Forbidden

        parent_type.delete_child(self._path.last_component)
