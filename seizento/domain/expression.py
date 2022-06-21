from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Union, Dict, Set

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


class FunctionParameterReference(Expression):
    def __init__(self, parameter: Identifier):
        self._parameter = parameter

    def evaluate(self, context: EvaluationContext) -> str:
        return context.function_arguments[self._parameter]


class DataNodeReference(Expression):
    def __init__(self, data_node_id: Path):
        self._data_node_id = data_node_id

    def get_root_node_names(self) -> Set[Identifier]:
        return {self._data_node_id.root}


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


class StringCast(Expression):
    def __init__(self, argument: Expression):
        self._argument = argument

    def serialize(self) -> str:
        return f'string({self._argument.serialize()})'


class Concatenation(Expression):
    def __init__(self, tokens: List[Expression]) -> None:
        self._tokens = tokens

    def serialize(self) -> str:
        return ' + '.join(token.serialize() for token in self._tokens)


class Template(Expression):
    def __init__(self, tokens: List[Expression]) -> None:
        self._tokens = tokens

    def as_concatenation(self) -> Concatenation:
        return Concatenation(
            tokens=[StringCast(token) for token in self._tokens]
        )
