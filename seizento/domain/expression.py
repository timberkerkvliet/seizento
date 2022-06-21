from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Union, Dict, Set, Any

from seizento.domain.identifier import Identifier
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
class EncryptedString:
    metadata: str
    value: str


@dataclass(frozen=True)
class PrimitiveLiteral(Expression):
    value: Union[str, EncryptedString, int, float, bool]

    def get_type(self) -> Type:
        if isinstance(self.value, str):
            return String()
        if isinstance(self.value, int):
            return Integer()

    def evaluate(self) -> Any:
        return self.value


@dataclass(frozen=True)
class PathReference(Expression):
    path: Path

    def get_type(self) -> Type:
        ...

    def evaluate(self) -> Any:
        ...
