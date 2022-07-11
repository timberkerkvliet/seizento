from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Set, Dict, Optional, Union

from seizento.path import PathComponent


class DataType(Enum):
    NULL = 'null'
    STRING = 'string'
    BOOL = 'boolean'
    FLOAT = 'float'
    INTEGER = 'integer'
    OBJECT = 'object'
    ARRAY = 'array'


class NewSchema:
    @abstractmethod
    def get_types(self) -> Set[DataType]:
        pass

    @abstractmethod
    def get_properties(self) -> Dict[str, NewSchema]:
        pass

    @abstractmethod
    def get_additional_properties(self) -> NewSchema:
        pass

    @abstractmethod
    def get_items(self) -> NewSchema:
        pass

    @property
    @abstractmethod
    def empty(self) -> bool:
        pass

    @abstractmethod
    def is_stricter_than(self, other: NewSchema):
        pass

    @abstractmethod
    def union(self, other: NewSchema):
        return other


@dataclass(frozen=True)
class EmptySchema(NewSchema):
    def is_stricter_than(self, other: NewSchema):
        return other.empty

    def union(self, other: NewSchema):
        return other

    def get_types(self) -> Set[DataType]:
        return set()

    def get_properties(self) -> Dict[str, NewSchema]:
        return {}

    def get_additional_properties(self) -> NewSchema:
        return self

    def get_items(self) -> NewSchema:
        return self

    def empty(self) -> bool:
        return True


@dataclass(frozen=True)
class ProperSchema(NewSchema):
    types: Set[DataType]
    properties: Dict[str, NewSchema] = field(default_factory=dict)
    additional_properties: NewSchema = field(default_factory=EmptySchema)
    items: NewSchema = field(default_factory=EmptySchema)

    def get_items(self) -> NewSchema:
        return self.items

    def get_types(self) -> Set[DataType]:
        return self.types

    def get_additional_properties(self) -> NewSchema:
        return self.additional_properties

    def get_properties(self) -> Dict[str, NewSchema]:
        return self.properties

    def is_stricter_than(self, other: NewSchema) -> bool:
        return self.types <= other.get_types() \
            and set(self.properties.keys()) >= set(other.get_properties().keys()) \
            and all(
                self.properties[prop].is_stricter_than(schema)
                for prop, schema in other.get_properties().items()
            ) \
            and self.additional_properties.is_stricter_than(other.get_additional_properties()) \
            and self.items.is_stricter_than(other.get_items())

    def union(self, other: NewSchema) -> NewSchema:
        return ProperSchema(
            types=self.types | other.get_types(),
            properties={
                prop: schema.union(other.get_properties()[prop])
                for prop, schema in self.properties.items()
                if prop in other.get_properties()
            },
            additional_properties=self.additional_properties.union(other.get_additional_properties()),
            items=self.items.union(other.get_items())
        )

    @property
    def empty(self) -> bool:
        return len(self.types) == 0 \
               and len(self.properties) == 0 \
               and self.additional_properties.empty \
               and self.items.empty

    def can_add_child(self, component: PathComponent) -> bool:
        return True

    def can_remove_child(self, component: PathComponent) -> bool:
        return True
