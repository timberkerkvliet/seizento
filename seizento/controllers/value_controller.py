from copy import deepcopy
from typing import Dict

from jsonschema.exceptions import ValidationError

from seizento.controllers.exceptions import Forbidden, NotFound

from seizento.path import Path
from seizento.app_data import AppData
from seizento.value import Value
from seizento.value_type import JsonValue


class ValueController:
    def __init__(
        self,
        path: Path,
        app_data: AppData
    ):
        self._path = path
        self._app_data = app_data

    def get(self) -> JsonValue:
        try:
            return self._app_data.value.navigate_to(self._path).value
        except (KeyError, IndexError):
            raise NotFound

    def delete(self) -> None:
        if len(self._path) == 0:
            raise Forbidden

        try:
            parent_value = self._app_data.value.navigate_to(self._path.remove_last())
            parent_schema = self._app_data.schema.navigate_to(self._path.remove_last())
        except (KeyError, IndexError):
            raise NotFound

        parent_value_copy = deepcopy(parent_value)
        parent_value_copy.delete_child(self._path.last_component)

        try:
            parent_schema.validate_value(parent_value_copy.value)
        except ValidationError as e:
            raise Forbidden('Delete would break validness of remaining schema against current value') from e

        parent_value.delete_child(component=self._path.last_component)

    def set(self, data: Dict) -> None:
        if len(self._path) == 0:
            raise Forbidden

        try:
            parent_value = self._app_data.value.navigate_to(self._path.remove_last())
            parent_schema = self._app_data.schema.navigate_to(self._path.remove_last())
        except (KeyError, IndexError):
            raise NotFound

        parent_value_copy = deepcopy(parent_value)
        parent_value_copy.set_child(self._path.last_component, value=Value(data))

        try:
            parent_schema.validate_value(parent_value_copy.value)
        except ValidationError as e:
            raise Forbidden('Is invalid for schema') from e

        parent_value.set_child(component=self._path.last_component, value=Value(data))
