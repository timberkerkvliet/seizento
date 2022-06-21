from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

from seizento.domain.identifier import Identifier
from seizento.domain.types.type import Type


@dataclass(frozen=True)
class Struct(Type):
    fields: Dict[Identifier, Type]

    @property
    def default_value(self) -> Optional[Dict]:
        return {
            field.name: field_type.default_value
            for field, field_type in self.fields.items()
        }

    def is_subtype(self, other: Type) -> bool:
        if not isinstance(other, Struct):
            return False

        return all(
            field_type.is_subtype(other.fields[field])
            for field, field_type in self.fields.items()
        )
