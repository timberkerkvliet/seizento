from typing import Callable, Any, Dict

from seizento.domain.path import PathComponent, PlaceHolder
from seizento.domain.types.type import Type


class Function(Type):
    def __init__(self, value_type: Type):
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

    @property
    def is_functional(self) -> bool:
        return True

    def get_subtypes(self) -> Dict[PathComponent, Type]:
        return {PlaceHolder(): self.value_type}
