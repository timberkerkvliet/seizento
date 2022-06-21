from dataclasses import dataclass
from typing import TypeVar

from seizento.domain.types.type import Type

T = TypeVar('T')


class Primitive(Type):
    @property
    def default_value(self):
        return None

    def is_subtype(self, other: Type) -> bool:
        return self == other


@dataclass(frozen=True)
class String(Primitive):
    pass


@dataclass(frozen=True)
class Boolean(Primitive):
    pass


@dataclass(frozen=True)
class Float(Primitive):
    pass


@dataclass(frozen=True)
class Integer(Primitive):
    pass

