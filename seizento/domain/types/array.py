from dataclasses import dataclass
from typing import List

from seizento.domain.types.type import Type


@dataclass(frozen=True)
class EmptyArray(Type):
    @property
    def default_value(self) -> List:
        return []

    def is_subtype(self, other: Type) -> bool:
        if isinstance(other, (EmptyArray, Array)):
            return True

        return False


@dataclass(frozen=True)
class Array(Type):
    value_type: Type

    @property
    def default_value(self) -> List:
        return []

    def is_subtype(self, other: Type) -> bool:
        if not isinstance(other, Array):
            return False

        return self.value_type.is_subtype(other.value_type)
