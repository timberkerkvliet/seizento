from __future__ import annotations
from dataclasses import dataclass
from typing import Union, Dict, Set, Any, TYPE_CHECKING

from seizento.data_tree import DataTree
from seizento.schema.primitives import String, Integer
from seizento.expression.expression import Expression
from seizento.path import Path, PathComponent
from seizento.schema.schema import Schema

if TYPE_CHECKING:
    from seizento.service.expression_service import ExpressionEvaluator


@dataclass(frozen=True)
class PrimitiveLiteral(Expression):
    value: Union[str, int, float, bool]

    def get_schema(self, schemas: Dict[Path, Schema]) -> Schema:
        if isinstance(self.value, str):
            return String()
        if isinstance(self.value, int):
            return Integer()

    async def evaluate(self, evaluator: ExpressionEvaluator, arguments: Dict[str, str]) -> Any:
        return self.value

    def get_path_references(self) -> Set[Path]:
        return set()

    def supports_child_at(self, component: PathComponent) -> bool:
        return False

    def to_tree(self) -> DataTree:
        return DataTree(root_data=self.value)
