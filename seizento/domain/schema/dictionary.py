from typing import Dict

from seizento.domain.schema.schema import Schema


class Dictionary(Schema):
    def __init__(self, value_type: Schema):
        self._value_type = value_type

    @property
    def value_type(self):
        return self._value_type

    @property
    def default_value(self) -> Dict:
        return {}

    def is_subschema(self, other: Schema) -> bool:
        if not isinstance(other, Dictionary):
            return False

        return self.value_type.is_subschema(other.value_type)

