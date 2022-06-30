from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Set, Any, TYPE_CHECKING

from seizento.data_tree import DataTree
from seizento.expression.expression import Expression
from seizento.path import Path, PathComponent
from seizento.schema.schema import Schema

if TYPE_CHECKING:
    from seizento.service.expression_service import ExpressionEvaluator


@dataclass(frozen=True)
class PathReference(Expression):
    reference: Path

    def get_schema(self, schemas: Dict[Path, Schema]) -> Schema:
        return schemas[self.reference]

    async def evaluate(self, evaluator: ExpressionEvaluator, arguments: Dict[str, str]) -> Any:
        return await evaluator.evaluate(path=self.reference)

    def get_path_references(self) -> Set[Path]:
        return {self.reference}

    def supports_child_at(self, component: PathComponent) -> bool:
        return False

    def to_tree(self) -> DataTree:
        return DataTree(root_data=self)
