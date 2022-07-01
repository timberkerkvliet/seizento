from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Set, Any, TYPE_CHECKING, FrozenSet, Union, List

from seizento.data_tree import DataTree
from seizento.expression.expression import Expression, Constraint, EvaluationResult, NO_CONSTRAINT
from seizento.identifier import Identifier
from seizento.path import Path, PathComponent, LiteralComponent, MatchComponent
from seizento.schema.schema import Schema

if TYPE_CHECKING:
    from seizento.service.expression_service import PathEvaluator


@dataclass(frozen=True)
class PathReference(Expression):
    reference: List[Union[LiteralComponent, Identifier]]

    @property
    def path(self) -> Path:
        return Path(
            components=tuple(
                x if isinstance(x, LiteralComponent) else MatchComponent()
                for x in self.reference
            )
        )

    def get_schema(self, schemas: Dict[Path, Schema]) -> Schema:
        return schemas[self.path]

    async def evaluate(
        self,
        evaluator: PathEvaluator,
        constraint: Constraint
    ) -> EvaluationResult:
        return EvaluationResult(
            {NO_CONSTRAINT: await evaluator.evaluate(path=self.path)}
        )

    def get_path_references(self) -> Set[Path]:
        return {self.path}

    def supports_child_at(self, component: PathComponent) -> bool:
        return False

    def to_tree(self) -> DataTree:
        return DataTree(root_data=self)
