from typing import Any

from seizento.domain.expression import Expression, PrimitiveLiteral, ArrayLiteral, ObjectLiteral, PathReference
from seizento.path import Path, StringComponent


def serialize_expression(value: Expression) -> Any:
    if isinstance(value, PrimitiveLiteral):
        return value.value

    if isinstance(value, ArrayLiteral):
        return [serialize_expression(x) for x in value.values]

    if isinstance(value, ObjectLiteral):
        return {x: serialize_expression(y) for x, y in value.values.items()}

    raise TypeError(type(value))


def parse_expression(value: Any) -> Expression:
    if isinstance(value, list):
        return ArrayLiteral(values=tuple(parse_expression(x) for x in value))

    if isinstance(value, dict):
        return ObjectLiteral(values={x: parse_expression(y) for x, y in value.items()})

    if isinstance(value, int):
        return PrimitiveLiteral(value)

    if isinstance(value, str):
        if value == '{/0}':
            return PathReference(reference=Path(components=(StringComponent('0'),)))

        return PrimitiveLiteral(value)

    raise TypeError
