from typing import Dict

from seizento.domain.types.type import Type


class Dictionary(Type):
    def __init__(self, value_type: Type):
        self._value_type = value_type

    @property
    def value_type(self):
        return self._value_type

    @property
    def default_value(self) -> Dict:
        return {}

    def is_subtype(self, other: Type) -> bool:
        return self == other
