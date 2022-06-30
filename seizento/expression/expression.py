from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, Set, Any, TYPE_CHECKING

from seizento.data_tree import DataTree
from seizento.path import Path, PathComponent
from seizento.schema.schema import Schema

if TYPE_CHECKING:
    from seizento.service.expression_service import ExpressionEvaluator


class Expression(ABC):
    @abstractmethod
    def get_schema(self, schemas: Dict[Path, Schema]) -> Schema:
        pass

    @abstractmethod
    async def evaluate(self, evaluator: ExpressionEvaluator, arguments: Dict[str, str]) -> Any:
        pass

    @abstractmethod
    def get_path_references(self) -> Set[Path]:
        pass

    @abstractmethod
    def supports_child_at(self, component: PathComponent) -> bool:
        pass

    @abstractmethod
    def to_tree(self) -> DataTree:
        pass
