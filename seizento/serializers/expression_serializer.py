from typing import Any, Union

from seizento.expression.expression import Expression
from seizento.expression.parameter_reference import ParameterReference
from seizento.expression.parametrized_dictionary import ParametrizedDictionary
from seizento.expression.primitive_literal import PrimitiveLiteral
from seizento.expression.array_literal import ArrayLiteral
from seizento.expression.struct_literal import StructLiteral
from seizento.expression.path_reference import PathReference
from seizento.identifier import Identifier
from seizento.path import Path, LiteralComponent

from seizento.serializers.path_serializer import parse_path


def serialize_expression(value: Expression) -> Any:
    if isinstance(value, PrimitiveLiteral):
        return value.value

    if isinstance(value, ArrayLiteral):
        return [serialize_expression(x) for x in value.values]

    if isinstance(value, StructLiteral):
        return {x: serialize_expression(y) for x, y in value.values.items()}

    if isinstance(value, ParameterReference):
        return '{' + value.reference.name + '}'

    if isinstance(value, PathReference):
        return '{/' \
               + '/'.join(x.value if isinstance(x, LiteralComponent) else f'<{x.name}>'
                          for x in value.reference) \
               + '}'

    if isinstance(value, ParametrizedDictionary):
        return {
            '*parameter': value.parameter.name,
            '*property': serialize_expression(value.key),
            '*value': serialize_expression(value.value)
        }

    raise TypeError(type(value))


def parse_reference(value: str) -> Union[ParameterReference, PathReference]:
    if '/' not in value:
        return ParameterReference(reference=Identifier(value))

    parts = [part for part in value.split('/') if len(part) > 0]

    return PathReference(
        reference=[
            LiteralComponent(part) if '<' not in part else Identifier(part[1:-1])
            for part in parts
        ]
    )


def parse_expression(value: Any) -> Expression:
    if isinstance(value, list):
        return ArrayLiteral(values=list(parse_expression(x) for x in value))

    if isinstance(value, dict):
        if set(value.keys()) == {'*parameter', '*property', '*value'}:
            return ParametrizedDictionary(
                key=parse_expression(value['*property']),
                value=parse_expression(value['*value']),
                parameter=Identifier(value['*parameter'])
            )

        return StructLiteral(values={x: parse_expression(y) for x, y in value.items()})
    if isinstance(value, float):
        return PrimitiveLiteral(value)

    if isinstance(value, int):
        return PrimitiveLiteral(value)

    if isinstance(value, bool):
        return PrimitiveLiteral(value)

    if value is None:
        return PrimitiveLiteral(None)

    if isinstance(value, str):
        if value[0] == '{' and value[1] != '{' and value[-1] == '}':
            return parse_reference(value[1:-1])

        return PrimitiveLiteral(value.replace('{{', '{').replace('}}', '}'))

    raise TypeError
