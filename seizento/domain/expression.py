from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Union, Dict, Set, Any, Tuple

from seizento.domain.identifier import Identifier
from seizento.domain.schema.array import Array, EmptyArray
from seizento.domain.schema.dictionary import Dictionary
from seizento.domain.schema.primitives import String, Integer
from seizento.domain.schema.struct import Struct, EmptyStruct
from seizento.path import Path
from seizento.domain.schema.schema import Schema


@dataclass(frozen=True)
class EvaluationContext:
    function_arguments: Dict[Identifier, str]
    root_expressions: Dict[Identifier, Expression]


@dataclass(frozen=True)
class TypeContext:
    root_types: Dict[Identifier, Schema]


class Expression(ABC):
    @abstractmethod
    def get_type(self) -> Schema:
        pass

    @abstractmethod
    def evaluate(self) -> Any:
        pass


@dataclass(frozen=True)
class PrimitiveLiteral(Expression):
    value: Union[str, int, float, bool]

    def get_type(self) -> Schema:
        if isinstance(self.value, str):
            return String()
        if isinstance(self.value, int):
            return Integer()

    def evaluate(self) -> Any:
        return self.value


@dataclass(frozen=True)
class ArrayLiteral(Expression):
    values: Tuple[Expression, ...]

    def get_type(self) -> Schema:
        if len(self.values) == 0:
            return EmptyArray()

        return Array(value_type=self.values[0].get_type())

    def evaluate(self) -> Any:
        return [value.evaluate() for value in self.values]


@dataclass(frozen=True)
class ObjectLiteral(Expression):
    values: Dict[str, Expression]

    def get_type(self) -> Schema:
        if len(self.values) == 0:
            return EmptyStruct()

        return Struct(
            fields={Identifier(x): y.get_type() for x, y in self.values.items()}
        )

    def evaluate(self) -> Any:
        return {key: value.evaluate() for key, value in self.values.items()}
