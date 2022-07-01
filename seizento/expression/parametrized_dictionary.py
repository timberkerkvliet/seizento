from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Set, Any

from seizento.data_tree import DataTree
from seizento.identifier import Identifier
from seizento.schema.dictionary import Dictionary
from seizento.schema.struct import Struct, EmptyStruct
from seizento.expression.expression import Expression, Constraint
from seizento.path import Path, PathComponent, LiteralComponent
from seizento.schema.schema import Schema
from seizento.service.expression_service import PathEvaluator


@dataclass(frozen=True)
class ParametrizedDictionary(Expression):
    parameter: Identifier
    key: Expression
    value: Expression

    def get_schema(self, schemas: Dict[Path, Schema]) -> Schema:
        return Dictionary(value_type=self.value.get_schema(schemas))

    async def evaluate(self, evaluator: PathEvaluator, constraint: Constraint) -> Any:
        key_result = await self.key.evaluate(evaluator=evaluator, constraint=constraint)
        value_result = await self.value.evaluate(evaluator=evaluator, constraint=constraint)

        return key_result \
            .merge(other=value_result) \
            .aggregate(
                parameter=self.parameter,
                aggregate_function=lambda pairs: {p[0]: p[1] for p in pairs}
            )

    def get_path_references(self) -> Set[Path]:
        return self.key.get_path_references() | self.value.get_path_references()

    def supports_child_at(self, component: PathComponent) -> bool:
        return False

    def to_tree(self) -> DataTree:
        return DataTree(
            root_data=self,
            subtrees={
                LiteralComponent(str(name)): expression.to_tree()
                for name, expression in self.values.items()
            }
        )
