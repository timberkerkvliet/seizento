from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Optional, List, Callable, Any


from seizento.domain.path import Path, PlaceHolder, PathComponent


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
