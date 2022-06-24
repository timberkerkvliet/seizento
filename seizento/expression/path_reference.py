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
class PathReference(Expression):
    reference: Path

    def get_type(self,  schemas: Dict[Path, Schema]) -> Schema:
        return schemas[self.reference]

    def evaluate(self, values: Dict[Path, Any]) -> Any:
        return values[self.reference]

    def get_path_references(self) -> Set[Path]:
        return {self.reference}
