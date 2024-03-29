from copy import deepcopy
from typing import Dict

from jsonschema.exceptions import ValidationError

from seizento.controllers.exceptions import NotFound, Forbidden, BadRequest
from seizento.app_data import AppData

from seizento.schema import Schema, InvalidSchema

from seizento.path import Path


class SchemaController:
    def __init__(self, path: Path, app_data: AppData):
        self._path = path
        self._app_data = app_data

    def get(self) -> Dict:
        try:
            target_type = self._app_data.schema.navigate_to(self._path)
        except KeyError as e:
            raise NotFound from e

        return target_type.schema

    def _get_parent_schema(self) -> Schema:
        try:
            return self._app_data.schema.navigate_to(self._path.remove_last())
        except KeyError as e:
            raise NotFound from e

    def set(self, data: Dict) -> None:
        if len(self._path) == 0:
            raise Forbidden

        try:
            new_schema = Schema(data)
        except InvalidSchema as e:
            raise BadRequest('Invalid JSON schema') from e

        parent_schema = self._get_parent_schema()

        try:
            parent_value = self._app_data.value.navigate_to(self._path.remove_last())
        except (KeyError, IndexError):
            parent_schema.set_child(component=self._path.last_component, schema=new_schema)
            return

        parent_schema_copy = deepcopy(parent_schema)
        parent_schema_copy.set_child(component=self._path.last_component, schema=new_schema)

        try:
            parent_schema_copy.validate_value(parent_value.value)
        except ValidationError as e:
            raise Forbidden('Requested schema is does not validate against current value') from e

        parent_schema.set_child(component=self._path.last_component, schema=new_schema)

    def delete(self) -> None:
        if len(self._path) == 0:
            raise Forbidden

        parent_schema = self._get_parent_schema()

        try:
            parent_value = self._app_data.value.navigate_to(self._path.remove_last())
        except (KeyError, IndexError):
            parent_schema.delete_child(component=self._path.last_component)
            return

        parent_schema_copy = deepcopy(parent_schema)
        parent_schema_copy.delete_child(component=self._path.last_component)

        try:
            parent_schema_copy.validate_value(parent_value.value)
        except ValidationError as e:
            raise Forbidden('Delete would break validness of remaining schema') from e

        parent_schema.delete_child(component=self._path.last_component)
