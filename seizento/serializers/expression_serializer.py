from typing import Any

from seizento.domain.expression import Expression, PrimitiveLiteral, ArrayLiteral


def serialize_expression(value: Expression) -> Any:
    if isinstance(value, PrimitiveLiteral):
        return value.value

    if isinstance(value, ArrayLiteral):
        return [serialize_expression(x) for x in value.values]

    raise TypeError(type(value))


def parse_expression(value: Any) -> Expression:
    if isinstance(value, list):
        return ArrayLiteral(values=tuple(parse_expression(x) for x in value))

    if isinstance(value, int):
        return PrimitiveLiteral(value)

    if isinstance(value, str):
        return PrimitiveLiteral(value)

    raise TypeError
