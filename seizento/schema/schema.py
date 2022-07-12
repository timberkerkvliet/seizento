from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Set, Dict


class DataType(Enum):
    NULL = 'null'
    STRING = 'string'
    BOOL = 'boolean'
    FLOAT = 'number'
    INTEGER = 'integer'
    OBJECT = 'object'
    ARRAY = 'array'


ALL_TYPES = {
    DataType.NULL,
    DataType.STRING,
    DataType.BOOL,
    DataType.FLOAT,
    DataType.INTEGER,
    DataType.OBJECT,
    DataType.ARRAY
}


class Constraint(ABC):
    @abstractmethod
    def satisfies(self, other: Constraint):
        ...

    @abstractmethod
    def union(self, other: Constraint) -> Constraint:
        ...

    @abstractmethod
    def is_empty(self) -> bool:
        ...


@dataclass(frozen=True)
class EverythingAllowed(Constraint):
    def satisfies(self, other: Constraint):
        return other.is_empty()

    def union(self, other: Constraint):
        return self

    def is_empty(self) -> bool:
        return True


@dataclass(frozen=True)
class NotAllowed(Constraint):
    def satisfies(self, other: Constraint):
        return True

    def union(self, other: Constraint) -> Constraint:
        return other

    def is_empty(self) -> bool:
        return False


@dataclass(frozen=True)
class Schema(Constraint):
    types: Set[DataType]
    properties: Dict[str, Constraint] = field(default_factory=dict)
    additional_properties: Constraint = field(default_factory=EverythingAllowed)
    items: Constraint = field(default_factory=EverythingAllowed)

    def get_items(self) -> Constraint:
        return self.items

    def get_types(self) -> Set[DataType]:
        return self.types

    def get_additional_properties(self) -> Constraint:
        return self.additional_properties

    def get_properties(self) -> Dict[str, Constraint]:
        return self.properties

    def satisfies(self, other: Constraint) -> bool:
        if other == EverythingAllowed():
            return True
        if other == NotAllowed():
            return False

        assert isinstance(other, Schema)

        if not self.types <= other.get_types():
            return False

        if not self.items.satisfies(other.get_items()):
            return False

        for prop, schema in self.properties.items():
            if prop in other.properties:
                if not schema.satisfies(other.get_properties()[prop]):
                    return False
            else:
                if not schema.satisfies(other.additional_properties):
                    return False

        if not self.additional_properties.satisfies(other.get_additional_properties()):
            return False

        return True

    def union(self, other: Constraint) -> Constraint:
        if other == EverythingAllowed():
            return other
        if other == NotAllowed():
            return self

        if isinstance(other, Schema):
            return Schema(
                types=self.types | other.types,
                properties={
                    prop: schema.union(other.properties[prop])
                    for prop, schema in self.properties.items()
                    if prop in other.properties
                },
                additional_properties=self.additional_properties.union(other.additional_properties),
                items=self.items.union(other.items)
            )

    def is_empty(self) -> bool:
        return len(self.types) == 0 \
           and all(constraint.is_empty() for constraint in self.properties.values()) == 0 \
           and self.additional_properties.is_empty() \
           and self.items.is_empty()
