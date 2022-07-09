from dataclasses import dataclass
from typing import TypeVar, Optional

from seizento.path import PathComponent
from seizento.schema.schema import Schema

T = TypeVar('T')


class Primitive(Schema):
    @property
    def default_value(self):
        return None

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
    pass
