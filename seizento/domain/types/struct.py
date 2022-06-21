from __future__ import annotations
from typing import Dict, Optional

from seizento.domain.identifier import Identifier
from seizento.domain.types.type import Type


class Struct(Type):
    def __init__(self, fields: Dict[Identifier, Type]):
        self._fields = fields

    @property
    def fields(self) -> Dict[Identifier, Type]:
        return dict(self._fields)

    @property
    def default_value(self) -> Optional[Dict]:
        return {
            field.name: field_type.default_value
            for field, field_type in self._fields.items()
        }

    def is_subtype(self, other: Type) -> bool:
        return self == other
