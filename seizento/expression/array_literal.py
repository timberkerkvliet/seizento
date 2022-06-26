from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Set, Any, Tuple

from seizento.data_tree import DataTree
from seizento.schema.array import Array, EmptyArray
from seizento.expression.expression import Expression
from seizento.path import Path, PathComponent, StringComponent
from seizento.schema.schema import Schema


@dataclass(frozen=True)
class ArrayLiteral(Expression):
    values: Tuple[Expression, ...]

    def get_schema(self, schemas: Dict[Path, Schema]) -> Schema:
        if len(self.values) == 0:
            return EmptyArray()

        return Array(value_type=self.values[0].get_schema(schemas))

    def evaluate(self, values: Dict[Path, Any]) -> Any:
        return [value.evaluate(values) for value in self.values]

    def get_path_references(self) -> Set[Path]:
        return {reference for expression in self.values for reference in expression.get_path_references()}

    def supports_child_at(self, component: PathComponent) -> bool:
        if not isinstance(component, StringComponent):
            return False

        return component.value in {str(k) for k in range(len(self.values) + 1)}

    def to_tree(self) -> DataTree:
        return DataTree(
            root_data=self,
            subtrees={
                StringComponent(str(k)): child_expression.to_tree()
                for k, child_expression in enumerate(self.values)
            }
        )
