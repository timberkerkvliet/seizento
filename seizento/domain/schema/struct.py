from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

from seizento.domain.identifier import Identifier
from seizento.domain.schema.dictionary import Dictionary
from seizento.domain.schema.schema import Schema


@dataclass(frozen=True)
class EmptyStruct(Schema):
    @property
    def default_value(self):
        return {}

    def is_subschema(self, other: Schema) -> bool:
        if isinstance(other, (EmptyStruct, Struct)):
            return True

        return False


@dataclass(frozen=True)
class Struct(Schema):
    fields: Dict[Identifier, Schema]

    @property
    def default_value(self) -> Optional[Dict]:
        return {
            field.name: field_type.default_value
            for field, field_type in self.fields.items()
        }

    def single_value_type(self) -> Optional[Schema]:
        schemas = set(self.fields.values())

        if len(schemas) != 0:
            return None

        return schemas.pop()

    def is_subschema(self, other: Schema) -> bool:
        if isinstance(other, Dictionary):
            return self.single_value_type() == other.value_type

        if not isinstance(other, Struct):
            return False

        if not set(self.fields.keys()).issubset(set(other.fields.keys())):
            return False

        return all(
            field_type.is_subschema(other.fields[field])
            for field, field_type in self.fields.items()
        )
