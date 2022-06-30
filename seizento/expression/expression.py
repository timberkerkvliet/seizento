from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Set, Any, TYPE_CHECKING, FrozenSet

from seizento.data_tree import DataTree
from seizento.identifier import Identifier
from seizento.path import Path, PathComponent
from seizento.schema.schema import Schema

if TYPE_CHECKING:
    from seizento.service.expression_service import PathEvaluator


@dataclass(frozen=True)
class Argument:
    parameter: Identifier
    value: str


class Expression(ABC):
    @abstractmethod
    def get_schema(self, schemas: Dict[Path, Schema]) -> Schema:
        pass

    @abstractmethod
    async def evaluate(
        self,
        evaluator: PathEvaluator,
        arguments: FrozenSet[Argument]
    ) -> Dict[FrozenSet[Argument], Any]:
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
