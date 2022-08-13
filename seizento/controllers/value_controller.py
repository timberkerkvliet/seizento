from typing import Dict

from jsonschema.exceptions import ValidationError

from seizento.controllers.exceptions import Forbidden, NotFound, MethodNotAllowed

from seizento.path import Path
from seizento.application_data import ApplicationData
from seizento.value import Value
from seizento.value_type import JsonValue


class ValueController:
    def __init__(
        self,
        path: Path,
        root: ApplicationData
    ):
        self._path = path
        self._root = root

    def get(self) -> JsonValue:
        try:
            return self._root.value.navigate_to(self._path).value
        except (KeyError, IndexError):
            raise NotFound

    def delete(self) -> None:
        raise MethodNotAllowed

    def set(self, data: Dict) -> None:
        if len(self._path) == 0:
            raise Forbidden

        try:
            parent_value = self._root.value.navigate_to(self._path.remove_last())
            parent_schema = self._root.schema.navigate_to(self._path.remove_last())
        except KeyError:
            raise NotFound

        parent_value_copy = Value(parent_value.value)
        parent_value_copy.set_child(self._path.last_component, value=Value(data))

        try:
            parent_schema.validate_value(parent_value_copy.value)
        except ValidationError as e:
            raise Forbidden(str(e))

        parent_value.set_child(component=self._path.last_component, value=Value(data))
