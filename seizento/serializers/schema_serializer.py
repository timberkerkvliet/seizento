from typing import Any

from seizento.domain.identifier import Identifier
from seizento.domain.schema.schema import Schema
from seizento.domain.schema.struct import Struct
from seizento.domain.schema.array import Array
from seizento.domain.schema.dictionary import Dictionary
from seizento.domain.schema.primitives import String, Boolean, Integer, Float


NAMES = {
    Struct: 'object',
    Dictionary: 'object',
    Array: 'array',
    String: 'string',
    Integer: 'integer',
    Float: 'number',
    Boolean: 'boolean'
}


def serialize_schema(value: Schema) -> Any:
    result = {'type': NAMES[type(value)]}

    if isinstance(value, Struct):
        fields = {
            field.name: serialize_schema(field_type)
            for field, field_type in value.fields.items()
        }
        if len(fields) > 0:
            result['properties'] = fields

    if isinstance(value, Array):
        result['items'] = serialize_schema(value.value_type)

    if isinstance(value, Dictionary):
        result['additionalProperties'] = serialize_schema(value.value_type)

    return result


def parse_schema(value: Any) -> Schema:
    name = value['type']

    if name == NAMES[String]:
        return String()
    if name == NAMES[Integer]:
        return Integer()
    if name == NAMES[Float]:
        return Float()
    if name == NAMES[Boolean]:
        return Boolean()
    if name == NAMES[Array]:
        value_type = value['items']
        return Array(value_type=parse_schema(value_type))

    if name == NAMES[Struct] and 'additionalProperties' not in value:
        properties = value.get('properties') or {}
        return Struct(
            fields={
                Identifier(field): parse_schema(subtype)
                for field, subtype in properties.items()
            }
        )

    if name == NAMES[Dictionary]:
        return Dictionary(value_type=value['additionalProperties'])

    raise TypeError