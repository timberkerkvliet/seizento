from typing import Dict

from jsonschema.exceptions import ValidationError

from seizento.controllers.exceptions import NotFound, Forbidden, BadRequest
from seizento.application_data import ApplicationData

from seizento.schema import Schema, InvalidSchema

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

        try:
            new_schema = Schema(data)
        except InvalidSchema as e:
            raise BadRequest from e

        try:
            parent_schema = self._root.schema.navigate_to(self._path.remove_last())
        except (KeyError, IndexError):
            raise NotFound

        try:
            parent_value = self._root.value.navigate_to(self._path.remove_last())
        except (KeyError, IndexError):
            parent_schema.set_child(component=self._path.last_component, schema=new_schema)
            return

        parent_schema_copy = Schema(parent_schema.schema)
        parent_schema_copy.set_child(component=self._path.last_component, schema=new_schema)

        try:
            parent_schema.validate_value(parent_value.value)
        except ValidationError as e:
            raise Forbidden(str(e))

        parent_schema.set_child(component=self._path.last_component, schema=new_schema)

    def delete(self) -> None:
        if len(self._path) == 0:
            raise Forbidden

        parent_schema = self._get_parent_schema()
        parent_schema.delete_child(self._path.last_component)
