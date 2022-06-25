from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, Set, Any

from seizento.path import Path, PathComponent
from seizento.schema.schema import Schema


class Expression(ABC):
    @abstractmethod
    def get_schema(self, schemas: Dict[Path, Schema]) -> Schema:
        pass

    @abstractmethod
    def evaluate(self, values: Dict[Path, Any]) -> Any:
        pass

    @abstractmethod
    def get_path_references(self) -> Set[Path]:
        pass

    @abstractmethod
    def supports_child_at(self, component: PathComponent) -> bool:
        pass
