from __future__ import annotations

from dataclasses import dataclass
from typing import Set, TYPE_CHECKING, Union

from seizento.data_tree import DataTree
from seizento.expression.expression import Expression, Constraint, EvaluationResult, NO_CONSTRAINT
from seizento.identifier import Identifier
from seizento.path import Path, PathComponent, LiteralComponent, MatchComponent, EMPTY_PATH
from seizento.schema.schema import Schema

if TYPE_CHECKING:
    from seizento.service.expression_service import PathEvaluator


@dataclass(frozen=True)
class PathReference(Expression):
    reference: list[Union[LiteralComponent, Identifier]]

    @property
    def path(self) -> Path:
        return Path(
            components=tuple(
                x if isinstance(x, LiteralComponent) else MatchComponent()
                for x in self.reference
            )
        )

    def get_schema(self, schemas: dict[Path, Schema]) -> Schema:
        return schemas[self.path]

    def _map_to_result(self, value, parts) -> EvaluationResult:
        if len(parts) == 0:
            return EvaluationResult({NO_CONSTRAINT: value})

        part = parts[0]

        if isinstance(part, LiteralComponent):
            return self._map_to_result(value[part.value], parts=parts[1:])

        return EvaluationResult(
            {
                Constraint(values={part: key}): value
                for key, value in value.items()
            }
        )

    async def evaluate(
        self,
        evaluator: PathEvaluator,
        constraint: Constraint
    ) -> EvaluationResult:
        path = EMPTY_PATH

        for part in self.reference:
            if not isinstance(part, LiteralComponent):
                break
            path = path.append(part)

        return self._map_to_result(await evaluator.evaluate(path=path), parts=self.reference[len(path):])

    def get_path_references(self) -> Set[Path]:
        return {self.path}

    def supports_child_at(self, component: PathComponent) -> bool:
        return False

    def to_tree(self) -> DataTree:
        return DataTree(root_data=self)
