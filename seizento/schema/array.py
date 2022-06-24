from dataclasses import dataclass
from typing import List

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
