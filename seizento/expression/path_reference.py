from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Set, Any, TYPE_CHECKING, FrozenSet

from seizento.data_tree import DataTree
from seizento.expression.expression import Expression, Argument
from seizento.path import Path, PathComponent
from seizento.schema.schema import Schema

if TYPE_CHECKING:
    from seizento.service.expression_service import PathEvaluator


@dataclass(frozen=True)
class PathReference(Expression):
    reference: Path

    def get_schema(self, schemas: Dict[Path, Schema]) -> Schema:
        return schemas[self.reference]

    async def evaluate(
        self,
        evaluator: PathEvaluator,
        arguments: FrozenSet[Argument]
    ) -> Dict[FrozenSet[Argument], Any]:
        return {
            frozenset(): await evaluator.evaluate(path=self.reference)
        }

    def get_path_references(self) -> Set[Path]:
        return {self.reference}

    def supports_child_at(self, component: PathComponent) -> bool:
        return False

    def to_tree(self) -> DataTree:
        return DataTree(root_data=self)
