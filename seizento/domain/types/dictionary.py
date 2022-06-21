from typing import Dict

from seizento.path import PathComponent, PlaceHolder
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

    @property
    def is_functional(self) -> bool:
        return self.value_type.is_functional

    def get_subtypes(self) -> Dict[PathComponent, Type]:
        return {PlaceHolder(): self.value_type}
