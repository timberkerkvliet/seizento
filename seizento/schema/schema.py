from __future__ import annotations

from dataclasses import dataclass, field
from typing import Set, Dict

from seizento.schema.constraint import Constraint, EverythingAllowed, NotAllowed
from seizento.schema.types import DataType


@dataclass(frozen=True)
class Schema(Constraint):
    types: Set[DataType]
    properties: Dict[str, Constraint] = field(default_factory=dict)
    additional_properties: Constraint = field(default_factory=EverythingAllowed)
    items: Constraint = field(default_factory=EverythingAllowed)

    def satisfies(self, other: Constraint) -> bool:
        if other == EverythingAllowed():
            return True
        if other == NotAllowed():
            return False

        assert isinstance(other, Schema)

        if not self.types <= other.types:
            return False

        if not self.items.satisfies(other.items):
            return False

        for prop, schema in self.properties.items():
            if prop in other.properties:
                if not schema.satisfies(other.properties[prop]):
                    return False
            else:
                if not schema.satisfies(other.additional_properties):
                    return False

        if not self.additional_properties.satisfies(other.additional_properties):
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
