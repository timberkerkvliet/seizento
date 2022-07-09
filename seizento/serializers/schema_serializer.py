from typing import Any

from seizento.identifier import Identifier
from seizento.schema.schema import Schema
from seizento.schema.struct import Struct
from seizento.schema.array import Array
from seizento.schema.dictionary import Dictionary
from seizento.schema.primitives import String, Boolean, Integer, Float, Null


NAMES = {
    Struct: 'object',
    Dictionary: 'object',
    Array: 'array',
    String: 'string',
    Integer: 'integer',
    Float: 'number',
    Boolean: 'boolean',
    Null: 'null'
}


def serialize_schema(value: Schema) -> Any:
    if isinstance(value, String) and value.optional:
        return {'type': ['string', 'null']}

    if isinstance(value, Boolean) and value.optional:
        return {'type': ['boolean', 'null']}

    if isinstance(value, Float) and value.optional:
        return {'type': ['number', 'null']}

    if isinstance(value, Integer) and value.optional:
        return {'type': ['integer', 'null']}

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

    if isinstance(name, list) and 'null' in name and len(name) == 2:
        optional_type = {x for x in name if x != 'null'}.pop()
        if optional_type == NAMES[String]:
            return String(optional=True)
        if optional_type == NAMES[Integer]:
            return Integer(optional=True)
        if optional_type == NAMES[Float]:
            return Float(optional=True)
        if optional_type == NAMES[Boolean]:
            return Boolean(optional=True)

    if name == NAMES[String]:
        return String()
    if name == NAMES[Integer]:
        return Integer()
    if name == NAMES[Float]:
        return Float()
    if name == NAMES[Boolean]:
        return Boolean()
    if name == NAMES[Null]:
        return Null()
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
        return Dictionary(value_type=parse_schema(value['additionalProperties']))

    raise TypeError
