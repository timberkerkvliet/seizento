from __future__ import annotations
from abc import ABC, abstractmethod


class Type(ABC):
    @property
    @abstractmethod
    def default_value(self):
        pass

    @abstractmethod
    def is_subtype(self, other: Type) -> bool:
        pass
