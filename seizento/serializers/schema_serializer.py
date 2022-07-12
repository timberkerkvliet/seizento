from typing import Any

from seizento.identifier import Identifier
from seizento.schema.schema import Schema, DataType, Schema, NotAllowed, EverythingAllowed, Constraint, ALL_TYPES


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

    if 'type' not in value:
        types = ALL_TYPES
    elif isinstance(value['type'], list):
        types = {DataType(val) for val in value['type']}
    else:
        types = {DataType(value['type'])}

    return Schema(
        types=types,
        additional_properties=parse_constraint(value['additionalProperties'])
        if 'additionalProperties' in value else EverythingAllowed(),
        properties={
            prop: parse_constraint(val)
            for prop, val in value['properties'].items()
        } if 'properties' in value else {},
        items=parse_constraint(value['items']) if 'items' in value else EverythingAllowed()
    )
