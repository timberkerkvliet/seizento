from dataclasses import dataclass
from typing import TypeVar, Optional

from seizento.path import PathComponent
from seizento.schema.schema import Schema

T = TypeVar('T')


class Primitive(Schema):
    def is_subschema(self, other: Schema) -> bool:
        return self == other

    def can_add_child(self, component: PathComponent) -> bool:
        return False

    def can_remove_child(self, component: PathComponent) -> bool:
        return False

    def common_superschema(self, other: Schema) -> Optional[Schema]:
        return None


@dataclass(frozen=True)
class String(Primitive):
    optional: bool = False

    def is_subschema(self, other: Schema) -> bool:
        if not self.optional:
            return isinstance(other, String)

        return isinstance(other, (Null, String))


@dataclass(frozen=True)
class Boolean(Primitive):
    optional: bool = False


@dataclass(frozen=True)
class Float(Primitive):
    optional: bool = False


@dataclass(frozen=True)
class Integer(Primitive):
    optional: bool = False


@dataclass(frozen=True)
class Null(Primitive):
    def is_subschema(self, other: Schema) -> bool:
        if isinstance(other, Null):
            return True

        if isinstance(other, String) and other.optional:
            return True

        return False
