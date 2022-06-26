from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Set, Any

from seizento.data_tree import DataTree
from seizento.expression.expression import Expression
from seizento.path import Path, PathComponent
from seizento.schema.schema import Schema


@dataclass(frozen=True)
class PathReference(Expression):
    reference: Path

    def get_schema(self, schemas: Dict[Path, Schema]) -> Schema:
        return schemas[self.reference]

    def evaluate(self, values: Dict[Path, Any]) -> Any:
        return values[self.reference]

    def get_path_references(self) -> Set[Path]:
        return {self.reference}

    def supports_child_at(self, component: PathComponent) -> bool:
        return False

    def to_tree(self) -> DataTree:
        return DataTree(root_data=self)
