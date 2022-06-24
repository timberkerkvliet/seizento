from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Union, Dict, Set, Any, Tuple

from seizento.domain.identifier import Identifier
from seizento.domain.schema.array import Array, EmptyArray
from seizento.domain.schema.primitives import String, Integer
from seizento.domain.schema.struct import Struct, EmptyStruct
from seizento.path import Path
from seizento.domain.schema.schema import Schema


@dataclass(frozen=True)
class EvaluationContext:
    values: Dict[Path, Schema]
    schemas: Dict[Path, Schema]


@dataclass(frozen=True)
class TypeContext:
    schemas: Dict[Path, Schema]


class Expression(ABC):
    @abstractmethod
    def get_type(self, schemas: Dict[Path, Schema]) -> Schema:
        pass

    @abstractmethod
    def evaluate(self, values: Dict[Path, Any]) -> Any:
        pass

    @abstractmethod
    def get_path_references(self) -> Set[Path]:
        pass


@dataclass(frozen=True)
class PrimitiveLiteral(Expression):
    value: Union[str, int, float, bool]

    def get_type(self, schemas: Dict[Path, Schema]) -> Schema:
        if isinstance(self.value, str):
            return String()
        if isinstance(self.value, int):
            return Integer()

    def evaluate(self, values: Dict[Path, Any]) -> Any:
        return self.value

    def get_path_references(self) -> Set[Path]:
        return set()


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


@dataclass(frozen=True)
class PathReference(Expression):
    reference: Path

    def get_type(self,  schemas: Dict[Path, Schema]) -> Schema:
        return schemas[self.reference]

    def evaluate(self, values: Dict[Path, Any]) -> Any:
        return values[self.reference]

    def get_path_references(self) -> Set[Path]:
        return {self.reference}
