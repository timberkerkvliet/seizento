from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, Optional

from seizento.path import PathComponent


class Type(ABC):
    @property
    @abstractmethod
    def default_value(self):
        pass

    @property
    @abstractmethod
    def is_functional(self) -> bool:
        pass

    @abstractmethod
    def get_subtypes(self) -> Optional[Dict[PathComponent, Type]]:
        pass
