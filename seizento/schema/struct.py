from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

from seizento.identifier import Identifier
from seizento.path import PathComponent, LiteralComponent
from seizento.schema.dictionary import Dictionary
from seizento.schema.schema import Schema


@dataclass(frozen=True)
class EmptyStruct(Schema):
    @property
    def default_value(self):
        return {}

    def is_subschema(self, other: Schema) -> bool:
        if isinstance(other, (EmptyStruct, Struct)):
            return True

        return False

    def supports_child_at(self, component: PathComponent) -> bool:
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

        if len(schemas) != 1:
            return None

        return schemas.pop()

    def is_subschema(self, other: Schema) -> bool:
        if isinstance(other, Dictionary):
            return all(field_type.is_subschema(other.value_type) for field_type in self.fields.values())

        if not isinstance(other, Struct):
            return False

        if not set(self.fields.keys()).issubset(set(other.fields.keys())):
            return False

        return all(
            field_type.is_subschema(other.fields[field])
            for field, field_type in self.fields.items()
        )

    def supports_child_at(self, component: PathComponent) -> bool:
        return isinstance(component, LiteralComponent)

    def __hash__(self):
        return hash(frozenset(tuple(x) for x in self.fields.items()))
