from typing import Dict

from jsonschema.exceptions import ValidationError

from seizento.controllers.exceptions import NotFound, Forbidden, BadRequest
from seizento.application_data import ApplicationData

from seizento.schema import Schema

from seizento.path import Path


class SchemaController:
    def __init__(self, path: Path, root: ApplicationData):
        self._path = path
        self._root = root

    def get(self) -> Dict:
        try:
            target_type = self._root.schema.navigate_to(self._path)
        except KeyError as e:
            raise NotFound from e

        return target_type.schema

    def _get_parent_schema(self) -> Schema:
        try:
            return self._root.schema.navigate_to(self._path.remove_last())
        except KeyError as e:
            raise NotFound from e

    def set(self, data: Dict) -> None:
        if len(self._path) == 0:
            raise Forbidden

        parent_schema = self._get_parent_schema()
        try:
            new_schema = Schema(data)
        except Exception as e:
            raise BadRequest from e

        try:
            current_schema = parent_schema.get_child(self._path.last_component)
        except (KeyError, IndexError):
            current_schema = None

        try:
            parent_schema.set_child(
                component=self._path.last_component,
                schema=new_schema
            )
        except Exception as e:
            raise NotFound from e

        try:
            self._root.schema.validate_value(self._root.value.value)
        except ValidationError as e:
            if current_schema is not None:
                parent_schema.set_child(
                    component=self._path.last_component,
                    schema=current_schema
                )
            else:
                parent_schema.delete_child(self._path.last_component)

            raise Forbidden(str(e))

    def delete(self) -> None:
        if len(self._path) == 0:
            raise Forbidden

        parent_schema = self._get_parent_schema()
        parent_schema.delete_child(self._path.last_component)
