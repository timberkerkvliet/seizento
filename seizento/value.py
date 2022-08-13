from __future__ import annotations
from abc import ABC
from dataclasses import dataclass

from seizento.path import PathComponent, LiteralComponent, Path
from seizento.value_type import JsonValue


@dataclass
class Value(ABC):
    value: JsonValue

    def navigate_to(self, path: Path) -> Value:
        result = self
        for component in path:
            result = result.get_child(component)

        return result

    def get_child(self, component: PathComponent) -> Value:
        if isinstance(component, LiteralComponent) and isinstance(self.value, dict):
            return Value(value=self.value[component.value])
        if isinstance(component, LiteralComponent) and isinstance(self.value, list):
            return Value(value=self.value[int(component.value)])

        raise KeyError

    def set_child(self, component: PathComponent, value: Value) -> None:
        if isinstance(component, LiteralComponent) and isinstance(self.value, dict):
            self.value[component.value] = value.value
        if isinstance(component, LiteralComponent) and isinstance(self.value, list):
            index = int(component.value)
            if index < len(self.value):
                self.value[int(component.value)] = value.value
            elif index == len(self.value):
                self.value.append(value.value)
            else:
                raise IndexError

    def delete_child(self, component: PathComponent) -> None:
        if isinstance(component, LiteralComponent):
            del self.value[component.value]
