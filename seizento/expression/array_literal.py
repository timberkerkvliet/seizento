from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Set, Any, Tuple

from seizento.domain.schema.array import Array, EmptyArray
from seizento.expression.expression import Expression
from seizento.path import Path
from seizento.domain.schema.schema import Schema


@dataclass(frozen=True)
class ArrayLiteral(Expression):
    values: Tuple[Expression, ...]

    def get_type(self,  schemas: Dict[Path, Schema]) -> Schema:
        if len(self.values) == 0:
            return EmptyArray()

        return Array(value_type=self.values[0].get_type(schemas))

    def evaluate(self, values: Dict[Path, Any]) -> Any:
        return [value.evaluate(values) for value in self.values]

    def get_path_references(self) -> Set[Path]:
        return {reference for expression in self.values for reference in expression.get_path_references()}
