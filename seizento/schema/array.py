from dataclasses import dataclass
from typing import List, Optional

from seizento.path import PathComponent, PlaceHolder
from seizento.schema.schema import Schema


@dataclass(frozen=True)
class EmptyArray(Schema):
    @property
    def default_value(self) -> List:
        return []

    def is_subschema(self, other: Schema) -> bool:
        if isinstance(other, (EmptyArray, Array)):
            return True

        return False

    def supports_child_at(self, component: PathComponent) -> bool:
        return False

    def common_superschema(self, other: Schema) -> Optional[Schema]:
        return None


@dataclass(frozen=True)
class Array(Schema):
    value_type: Schema

    @property
    def default_value(self) -> List:
        return []

    def is_subschema(self, other: Schema) -> bool:
        if not isinstance(other, Array):
            return False

        return self.value_type.is_subschema(other.value_type)

    def supports_child_at(self, component: PathComponent) -> bool:
        return isinstance(component, PlaceHolder)

    def common_superschema(self, other: Schema) -> Optional[Schema]:
        return None
