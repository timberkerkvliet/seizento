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

    def supports_child_at(self, component: PathComponent) -> bool:
        return False

    def common_superschema(self, other: Schema) -> Optional[Schema]:
        return None


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

