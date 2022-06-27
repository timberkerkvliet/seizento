from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Set, Any

from seizento.data_tree import DataTree
from seizento.identifier import Identifier
from seizento.schema.struct import Struct, EmptyStruct
from seizento.expression.expression import Expression
from seizento.path import Path, PathComponent, LiteralComponent
from seizento.schema.schema import Schema


@dataclass(frozen=True)
class StructLiteral(Expression):
    values: Dict[str, Expression]

    def get_schema(self, schemas: Dict[Path, Schema]) -> Schema:
        if len(self.values) == 0:
            return EmptyStruct()

        return Struct(
            fields={Identifier(x): y.get_schema(schemas) for x, y in self.values.items()}
        )

    def evaluate(self, values: Dict[Path, Any]) -> Any:
        return {key: value.evaluate(values) for key, value in self.values.items()}

    def get_path_references(self) -> Set[Path]:
        return {
            reference for expression in self.values.values()
            for reference in expression.get_path_references()
        }

    def supports_child_at(self, component: PathComponent) -> bool:
        if not isinstance(component, LiteralComponent):
            return False

        return component.value in self.values

    def to_tree(self) -> DataTree:
        return DataTree(
            root_data=self,
            subtrees={
                LiteralComponent(str(name)): expression.to_tree()
                for name, expression in self.values.items()
            }
        )
