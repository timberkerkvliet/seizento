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
    FLOAT = 'number'
    INTEGER = 'integer'
    OBJECT = 'object'
    ARRAY = 'array'


class Schema:
    @abstractmethod
    def get_types(self) -> Set[DataType]:
        pass

    @abstractmethod
    def get_properties(self) -> Dict[str, Schema]:
        pass

    @abstractmethod
    def get_additional_properties(self) -> Schema:
        pass

    @abstractmethod
    def get_items(self) -> Schema:
        pass

    @property
    @abstractmethod
    def empty(self) -> bool:
        pass

    @abstractmethod
    def conforms_to(self, other: Schema):
        pass

    @abstractmethod
    def union(self, other: Schema):
        return other


@dataclass(frozen=True)
class EmptySchema(Schema):
    def conforms_to(self, other: Schema):
        return other.empty

    def union(self, other: Schema):
        return self

    def get_types(self) -> Set[DataType]:
        return set()

    def get_properties(self) -> Dict[str, Schema]:
        return {}

    def get_additional_properties(self) -> Schema:
        return self

    def get_items(self) -> Schema:
        return self

    def empty(self) -> bool:
        return True


@dataclass(frozen=True)
class ImpossibleSchema(Schema):
    def conforms_to(self, other: Schema):
        return True

    def union(self, other: Schema):
        return other

    def get_types(self) -> Set[DataType]:
        return set()

    def get_properties(self) -> Dict[str, Schema]:
        return {}

    def get_additional_properties(self) -> Schema:
        return self

    def get_items(self) -> Schema:
        return self

    def empty(self) -> bool:
        return False


@dataclass(frozen=True)
class ProperSchema(Schema):
    types: Set[DataType]
    properties: Dict[str, Schema] = field(default_factory=dict)
    additional_properties: Schema = field(default_factory=EmptySchema)
    items: Schema = field(default_factory=EmptySchema)

    def get_items(self) -> Schema:
        return self.items

    def get_types(self) -> Set[DataType]:
        return self.types

    def get_additional_properties(self) -> Schema:
        return self.additional_properties

    def get_properties(self) -> Dict[str, Schema]:
        return self.properties

    def conforms_to(self, other: Schema) -> bool:
        if not self.types <= other.get_types() or not self.items.conforms_to(other.get_items()):
            return False

        for prop, schema in self.properties.items():
            if prop in other.get_properties():
                if not schema.conforms_to(other.get_properties()[prop]):
                    return False
            else:
                if not schema.conforms_to(other.get_additional_properties()):
                    return False

        if not self.additional_properties.conforms_to(other.get_additional_properties()):
            return False

        return True

    def union(self, other: Schema) -> Schema:
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
