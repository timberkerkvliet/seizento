from __future__ import annotations
from dataclasses import dataclass
from typing import Union, Dict, Set, Any

from seizento.schema.primitives import String, Integer
from seizento.expression.expression import Expression
from seizento.path import Path
from seizento.schema.schema import Schema


@dataclass(frozen=True)
class PrimitiveLiteral(Expression):
    value: Union[str, int, float, bool]

    def get_type(self, schemas: Dict[Path, Schema]) -> Schema:
        if isinstance(self.value, str):
            return String()
        if isinstance(self.value, int):
            return Integer()

    def evaluate(self, values: Dict[Path, Any]) -> Any:
        return self.value

    def get_path_references(self) -> Set[Path]:
        return set()

    def supports_child_at(self, component: PathComponent) -> bool:
        return False

