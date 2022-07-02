from typing import Any

from seizento.expression.expression import Expression
from seizento.expression.primitive_literal import PrimitiveLiteral
from seizento.expression.array_literal import ArrayLiteral
from seizento.expression.struct_literal import StructLiteral
from seizento.expression.path_reference import PathReference
from seizento.path import Path, LiteralComponent
from seizento.serializers.path_serializer import parse_path


def serialize_expression(value: Expression) -> Any:
    if isinstance(value, PrimitiveLiteral):
        return value.value

    if isinstance(value, ArrayLiteral):
        return [serialize_expression(x) for x in value.values]

    if isinstance(value, StructLiteral):
        return {x: serialize_expression(y) for x, y in value.values.items()}

    raise TypeError(type(value))


def parse_expression(value: Any) -> Expression:
    if isinstance(value, list):
        return ArrayLiteral(values=tuple(parse_expression(x) for x in value))

    if isinstance(value, dict):
        return StructLiteral(values={x: parse_expression(y) for x, y in value.items()})

    if isinstance(value, int):
        return PrimitiveLiteral(value)

    if isinstance(value, bool):
        return PrimitiveLiteral(value)

    if isinstance(value, str):
        if value[0] == '{' and value[1] != '{' and value[-1] == '}':
            return PathReference(reference=parse_path(value[1:-1]))

        return PrimitiveLiteral(value.replace('{{', '{').replace('}}', '}'))

    raise TypeError
