from dataclasses import dataclass
from typing import TypeVar

from seizento.schema.schema import Schema

T = TypeVar('T')


class Primitive(Schema):
    @property
    def default_value(self):
        return None

    def is_subschema(self, other: Schema) -> bool:
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

