from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Set, Any

from seizento.expression.expression import Expression
from seizento.path import Path
from seizento.domain.schema.schema import Schema


@dataclass(frozen=True)
class PathReference(Expression):
    reference: Path

    def get_type(self,  schemas: Dict[Path, Schema]) -> Schema:
        return schemas[self.reference]

    def evaluate(self, values: Dict[Path, Any]) -> Any:
        return values[self.reference]

    def get_path_references(self) -> Set[Path]:
        return {self.reference}
