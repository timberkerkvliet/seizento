from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Union, Dict, Set, Any, Tuple

from seizento.domain.identifier import Identifier
from seizento.domain.schema.array import Array, EmptyArray
from seizento.domain.schema.primitives import String, Integer
from seizento.domain.schema.struct import Struct, EmptyStruct
from seizento.expression.expression import Expression
from seizento.path import Path
from seizento.domain.schema.schema import Schema


@dataclass(frozen=True)
class ObjectLiteral(Expression):
    values: Dict[str, Expression]

    def get_type(self,  schemas: Dict[Path, Schema]) -> Schema:
        if len(self.values) == 0:
            return EmptyStruct()

        return Struct(
            fields={Identifier(x): y.get_type(schemas) for x, y in self.values.items()}
        )

    def evaluate(self, values: Dict[Path, Any]) -> Any:
        return {key: value.evaluate(values) for key, value in self.values.items()}

    def get_path_references(self) -> Set[Path]:
        return {
            reference for expression in self.values.values()
            for reference in expression.get_path_references()
        }

