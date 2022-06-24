from __future__ import annotations
from abc import ABC, abstractmethod


class Schema(ABC):
    @property
    @abstractmethod
    def default_value(self):
        pass

    @abstractmethod
    def is_subschema(self, other: Schema) -> bool:
        pass
