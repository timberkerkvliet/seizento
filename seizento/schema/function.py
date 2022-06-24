from typing import Callable, Any

from seizento.schema.schema import Schema


class Function(Schema):
    def __init__(self, value_type: Schema):
        self._value_type = value_type

    @property
    def value_type(self):
        return self._value_type

    @staticmethod
    def _default_function(arg: str):
        raise KeyError

    @property
    def default_value(self) -> Callable[[str], Any]:
        return self._default_function

    def is_subschema(self, other: Schema) -> bool:
        if not isinstance(other, Function):
            return False

        return self.value_type.is_subschema(other.value_type)

