from __future__ import annotations
from abc import ABC, abstractmethod

from seizento.path import PathComponent


class Schema(ABC):
    @property
    @abstractmethod
    def default_value(self):
        pass

    @abstractmethod
    def is_subschema(self, other: Schema) -> bool:
        pass

    @abstractmethod
    def supports_child_at(self, component: PathComponent) -> bool:
        pass
