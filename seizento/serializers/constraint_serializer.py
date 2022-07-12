from typing import Any

from seizento.schema.schema import Schema
from seizento.schema.constraint import Constraint, EverythingAllowed, NotAllowed
from seizento.schema.types import DataType


def serialize_constraint(value: Constraint) -> Any:
    if value == NotAllowed:
        return False
    if value == EverythingAllowed:
        return True

    assert isinstance(value, Schema)

    result = {}

    if len(value.types) == 1:
        result['type'] = value.types.pop().value

    if len(value.types) > 1:
        result['type'] = [data_type.value for data_type in value.types]

    if len(value.properties) > 0:
        result['properties'] = {
            prop: serialize_constraint(constraint)
            for prop, constraint in value.properties.items()
            if not constraint.is_empty()
        }

    if not value.items.is_empty():
        result['items'] = serialize_constraint(value.items)

    if not value.additional_properties.is_empty():
        result['additionalProperties'] = serialize_constraint(value.additional_properties)

    return result


def parse_constraint(value: Any) -> Constraint:
    if value is False:
        return NotAllowed()

    if value is True:
        return EverythingAllowed()

    kwargs = {}

    if 'type' in value:
        if isinstance(value['type'], list):
            kwargs['types'] = {DataType(val) for val in value['type']}
        else:
            kwargs['types'] = {DataType(value['type'])}

    if 'additionalProperties' in value:
        kwargs['additional_properties'] = parse_constraint(value['additionalProperties'])

    if 'properties' in value:
        kwargs['properties'] = {
            prop: parse_constraint(val)
            for prop, val in value['properties'].items()
        }

    if 'items' in value:
        kwargs['items'] = parse_constraint(value['items'])

    return Schema(**kwargs)
