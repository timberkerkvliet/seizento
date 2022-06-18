from __future__ import annotations
import json
from abc import ABC, abstractmethod
from typing import List, Tuple, Union, Dict


class Arguments(ABC):
    @abstractmethod
    def get(self, parameter: str) -> str:
        ...


class Expression(ABC):
    @abstractmethod
    def evaluate(self, arguments: Arguments):
        ...

    @abstractmethod
    def serialize(self) -> str:
        ...


class ParameterReference(Expression):
    def __init__(self, parameter: str):
        self._parameter = parameter

    def evaluate(self, arguments: Arguments):
        return arguments.get(parameter=self._parameter)

    def serialize(self) -> str:
        return self._parameter


class DataReference(Expression):
    def __init__(self, root: str, path: List[Template]):
        self._root = root
        self._path = path

    def evaluate(self, arguments: Arguments):
        return arguments.get(parameter=self.serialize())

    def serialize(self) -> str:
        elements = [self._root] + [identifier.serialize(start='<', end='>') for identifier in self._path]
        return '/'.join(elements)


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
