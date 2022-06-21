from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Union, Dict, Set, Any, Tuple

from seizento.domain.identifier import Identifier
from seizento.domain.types.array import Array, EmptyArray
from seizento.domain.types.primitives import String, Integer
from seizento.path import Path
from seizento.domain.types.type import Type


@dataclass(frozen=True)
class EvaluationContext:
    function_arguments: Dict[Identifier, str]
    root_expressions: Dict[Identifier, Expression]


@dataclass(frozen=True)
class TypeContext:
    root_types: Dict[Identifier, Type]


class Expression(ABC):
    @abstractmethod
    def get_type(self) -> Type:
        pass

    @abstractmethod
    def evaluate(self) -> Any:
        pass


@dataclass(frozen=True)
class PrimitiveLiteral(Expression):
    value: Union[str, int, float, bool]

    def get_type(self) -> Type:
        if isinstance(self.value, str):
            return String()
        if isinstance(self.value, int):
            return Integer()

    def evaluate(self) -> Any:
        return self.value


@dataclass(frozen=True)
class ArrayLiteral(Expression):
    values: Tuple[Expression, ...]

    def get_type(self) -> Type:
        if len(self.values) == 0:
            return EmptyArray()

        return Array(value_type=self.values[0].get_type())

    def evaluate(self) -> Any:
        return [value.evaluate() for value in self.values]
