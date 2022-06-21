from dataclasses import dataclass
from typing import Dict, List

from seizento.path import PathComponent, PlaceHolder
from seizento.domain.types.type import Type


@dataclass(frozen=True)
class Array(Type):
    value_type: Type

    @property
    def default_value(self) -> List:
        return []

    @property
    def is_functional(self) -> bool:
        return self.value_type.is_functional

    def get_subtypes(self) -> Dict[PathComponent, Type]:
        return {
            PlaceHolder(): self.value_type
        }
