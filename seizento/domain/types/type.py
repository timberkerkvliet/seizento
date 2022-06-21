from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Optional

from seizento.path import PathComponent


class Type(ABC):
    @property
    @abstractmethod
    def default_value(self):
        pass


@dataclass(frozen=True)
class Any(Type):
    @property
    def default_value(self):
        raise None

    @property
    def is_functional(self) -> bool:
        return False

    def get_subtypes(self) -> Optional[Dict[PathComponent, Type]]:
        pass
