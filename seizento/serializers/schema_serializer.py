from typing import Any

from seizento.domain.identifier import Identifier
from seizento.domain.schema.schema import Schema
from seizento.domain.schema.struct import Struct
from seizento.domain.schema.array import Array
from seizento.domain.schema.dictionary import Dictionary
from seizento.domain.schema.function import Function
from seizento.domain.schema.primitives import String, Boolean, Integer, Float


NAMES = {
    Struct: 'STRUCT',
    Dictionary: 'DICTIONARY',
    Array: 'ARRAY',
    Function: 'FUNCTION',
    String: 'STRING',
    Integer: 'INTEGER',
    Float: 'FLOAT',
    Boolean: 'BOOLEAN'
}


def serialize_schema(value: Schema) -> Any:
    result = {
        'type': NAMES[type(value)]
    }

    if isinstance(value, Struct):
        fields = {
            field.name: serialize_schema(field_type)
            for field, field_type in value.fields.items()
        }
        if len(fields) > 0:
            result['fields'] = fields

    if isinstance(value, (Array, Function, Dictionary)):
        result['value_type'] = serialize_schema(value.value_type)

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
    if name in {NAMES[Array], NAMES[Dictionary], NAMES[Function]}:
        value_type = value['value_type']

        if name == NAMES[Array]:
            return Array(
                value_type=parse_schema(value_type)
            )
        if name == NAMES[Dictionary]:
            return Dictionary(
                value_type=parse_schema(value_type)
            )
        if name == NAMES[Function]:
            return Function(
                value_type=parse_schema(value_type)
            )
    if name == NAMES[Struct]:
        if 'fields' not in value:
            return Struct(fields={})

        return Struct(
            fields={
                Identifier(field): parse_schema(subtype)
                for field, subtype in value['fields'].items()
            }
        )
