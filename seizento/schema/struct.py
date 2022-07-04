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
        if isinstance(other, (EmptyStruct, Struct, Dictionary)):
            return True

        return False

    def can_add_child(self, component: PathComponent) -> bool:
        return False

    def can_remove_child(self, component: PathComponent) -> bool:
        return False

    def common_superschema(self, other: Schema) -> Optional[Schema]:
        if isinstance(other, (EmptyStruct, Struct, Dictionary)):
            return other

        return None


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

    def can_add_child(self, component: PathComponent) -> bool:
        return isinstance(component, LiteralComponent)

    def can_remove_child(self, component: PathComponent) -> bool:
        return isinstance(component, LiteralComponent)

    def __hash__(self):
        return hash(frozenset(tuple(x) for x in self.fields.items()))

    def common_superschema(self, other: Schema) -> Optional[Schema]:
        if isinstance(other, EmptyStruct):
            return self

        if isinstance(other, Dictionary) and self.single_value_type() == other.value_type:
            return other

        if not isinstance(other, Struct):
            return None

        if self.single_value_type() == other.single_value_type():
            return Dictionary(value_type=self.single_value_type())
