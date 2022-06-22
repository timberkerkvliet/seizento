from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

from seizento.domain.identifier import Identifier
from seizento.domain.schema.schema import Schema


@dataclass(frozen=True)
class Struct(Schema):
    fields: Dict[Identifier, Schema]

    @property
    def default_value(self) -> Optional[Dict]:
        return {
            field.name: field_type.default_value
            for field, field_type in self.fields.items()
        }

    def is_subschema(self, other: Schema) -> bool:
        if not isinstance(other, Struct):
            return False

        if set(self.fields.keys()) != set(other.fields.keys()):
            return False

        return all(
            field_type.is_subschema(other.fields[field])
            for field, field_type in self.fields.items()
        )
