from __future__ import annotations
from typing import Dict, Optional

from seizento.domain.identifier import Identifier
from seizento.path import StringComponent, PathComponent
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

    @property
    def is_functional(self) -> bool:
        return any(field_type.is_functional for field_type in self._fields.values())

    def __eq__(self, other) -> bool:
        if not isinstance(other, Struct):
            return False

        return self.fields == other.fields

    def get_subtypes(self) -> Dict[PathComponent, Type]:
        return {
            StringComponent(value=field.name): field_type
            for field, field_type in self._fields.items()
        }
