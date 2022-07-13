from __future__ import annotations

from dataclasses import dataclass, field
from typing import Set, Dict

from seizento.path import PathComponent, LiteralComponent, PropertyPlaceHolder, IndexPlaceHolder, PlaceHolder
from seizento.schema.constraint import Constraint, EverythingAllowed, NotAllowed
from seizento.schema.types import DataType, ALL_TYPES


@dataclass
class Schema(Constraint):
    types: Set[DataType] = field(default_factory=lambda: ALL_TYPES)
    properties: Dict[str, Constraint] = field(default_factory=dict)
    additional_properties: Constraint = field(default_factory=EverythingAllowed)
    items: Constraint = field(default_factory=EverythingAllowed)

    def satisfies(self, other: Constraint) -> bool:
        if other == EverythingAllowed():
            return True
        if other == NotAllowed():
            return False

        assert isinstance(other, Schema)

        return self.types <= other.types \
            and self.items.satisfies(other.items) \
            and self.additional_properties.satisfies(other.additional_properties) \
            and all(
                schema.satisfies(other.properties[prop])
                if prop in other.properties else schema.satisfies(other.additional_properties)
                for prop, schema in self.properties.items()
            )

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

    def intersection(self, other: Constraint) -> Constraint:
        if other == EverythingAllowed():
            return self
        if other == NotAllowed():
            return other

        assert isinstance(other, Schema)

        return Schema(
            types=self.types & other.types,
            properties={
                prop: schema.intersection(other.properties[prop])
                for prop, schema in self.properties.items()
                if prop in other.properties
            },
            additional_properties=self.additional_properties.intersection(other.additional_properties),
            items=self.items.intersection(other.items)
        )

    def is_empty(self) -> bool:
        return len(self.types) == 0 \
           and all(constraint.is_empty() for constraint in self.properties.values()) == 0 \
           and self.additional_properties.is_empty() \
           and self.items.is_empty()

    def get_child(self, component: PathComponent) -> Constraint:
        candidates = []
        if isinstance(component, LiteralComponent) and component.value in self.properties:
            candidates.append(self.properties[component.value])
        if component == IndexPlaceHolder():
            candidates.append(self.items)
        if component == PropertyPlaceHolder():
            candidates.append(self.additional_properties)
        if isinstance(component, LiteralComponent) and component.value.isdigit():
            candidates.append(self.items)
        if isinstance(component, LiteralComponent):
            candidates.append(self.additional_properties)
        if component == PlaceHolder():
            candidates = list(self.properties.values()) + [self.items, self.additional_properties]

        constraints = [x for x in candidates if x != NotAllowed()]
        result = EverythingAllowed()
        for x in constraints:
            result = result.intersection(x)

        return result

    def set_child(self, component: PathComponent, constraint: Constraint) -> None:
        if isinstance(component, LiteralComponent):
            self.properties[component.value] = constraint
        if component == PropertyPlaceHolder():
            self.additional_properties = constraint
        if component == IndexPlaceHolder():
            self.items = constraint

    def delete_child(self, component: PathComponent) -> None:
        if isinstance(component, LiteralComponent):
            self.properties.pop(component.value, None)
