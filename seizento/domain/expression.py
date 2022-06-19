from __future__ import annotations
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Union, Dict, Set

from seizento.domain.identifier import Identifier, Path
from seizento.domain.type import Type, String


@dataclass(frozen=True)
class EvaluationContext:
    function_arguments: Dict[Identifier, str]
    root_expressions: Dict[Identifier, Expression]


@dataclass(frozen=True)
class TypeContext:
    root_types: Dict[Identifier, Type]


class Expression(ABC):
    @abstractmethod
    def evaluate(self, context: EvaluationContext):
        ...

    @abstractmethod
    def type(self, context: TypeContext) -> Type:
        ...

    @abstractmethod
    def get_node(self, data_node_identifier: Path) -> Expression:
        ...

    @abstractmethod
    def get_root_node_names(self) -> Set[Identifier]:
        ...


class FunctionParameterReference(Expression):
    def __init__(self, parameter: Identifier):
        self._parameter = parameter

    def evaluate(self, context: EvaluationContext) -> str:
        return context.function_arguments[self._parameter]

    def type(self, context: TypeContext) -> String:
        return String(optional=False, secret=False)


class DataNodeReference(Expression):
    def __init__(self, data_node_id: Path):
        self._data_node_id = data_node_id

    def evaluate(self, context: EvaluationContext):
        return context \
            .root_expressions[self._data_node_id.root] \
            .get_node(self._data_node_id.path_as_identifier) \
            .evaluate(context=context)

    def get_root_node_names(self) -> Set[Identifier]:
        return {self._data_node_id.root}


class Literal(Expression):
    def __init__(self, value: Union[str, int, float, bool]) -> None:
        self._value = value

    def evaluate(self, arguments: Arguments) -> str:
        return self._value

    def serialize(self) -> str:
        return str(self._value)


class StringCast(Expression):
    def __init__(self, argument: Expression):
        self._argument = argument

    def evaluate(self, arguments: Arguments) -> str:
        evaluated_argument = self._argument.evaluate(arguments)

        if isinstance(evaluated_argument, str):
            return evaluated_argument

        if isinstance(evaluated_argument, int):
            return str(evaluated_argument)

        if isinstance(evaluated_argument, bool):
            return 'true' if evaluated_argument else 'false'

        if isinstance(evaluated_argument, float):
            return str(evaluated_argument)

        if isinstance(evaluated_argument, (Dict, List)):
            return json.dumps(evaluated_argument)

    def serialize(self) -> str:
        return f'string({self._argument.serialize()})'


class Concatenation(Expression):
    def __init__(self, tokens: List[Expression]) -> None:
        self._tokens = tokens

    def evaluate(self, arguments: Arguments) -> str:
        return ''.join(
            token.evaluate(arguments)
            for token in self._tokens
        )

    def serialize(self) -> str:
        return ' + '.join(token.serialize() for token in self._tokens)


class Template(Expression):
    def __init__(self, tokens: List[Expression]) -> None:
        self._tokens = tokens

    def as_concatenation(self) -> Concatenation:
        return Concatenation(
            tokens=[StringCast(token) for token in self._tokens]
        )

    def evaluate(self, arguments: Arguments) -> str:
        return self.as_concatenation().evaluate(arguments)

    def serialize(self, start='{', end='}') -> str:
        return ''.join(
            token.serialize() if isinstance(token, Literal) else start + token.serialize() + end
            for token in self._tokens
        )

expr = Template(
    tokens=[
        Literal('hey'),
        DataReference(
            root='basic-seizento',
            path=[Template(tokens=[Literal('tenant-id-'), ParameterReference('tenant_id')])]
        )
    ]
)

print(expr.serialize())
