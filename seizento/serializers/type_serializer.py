from typing import Any

from seizento.domain.identifier import Identifier
from seizento.domain.types.type import Type
from seizento.domain.types.struct import Struct
from seizento.domain.types.array import Array
from seizento.domain.types.dictionary import Dictionary
from seizento.domain.types.function import Function
from seizento.domain.types.primitives import String, Boolean, Integer, Float


def serialize_type(value: Type) -> Any:
    result = serialize_root_data(value)

    if isinstance(value, Struct):
        fields = {
            field.name: serialize_type(field_type)
            for field, field_type in value.fields.items()
        }
        if len(fields) > 0:
            result['fields'] = fields

    if isinstance(value, (Array, Function, Dictionary)):
        result['value_type'] = serialize_type(value.value_type)

    return result


def serialize_root_data(value: Type):
    if isinstance(value, Struct):
        return {'name': 'STRUCT'}
    if isinstance(value, Dictionary):
        return {'name': 'DICTIONARY'}
    if isinstance(value, Array):
        return {'name': 'ARRAY'}
    if isinstance(value, Function):
        return {'name': 'FUNCTION'}
    if isinstance(value, String):
        return {'name': 'STRING'}
    if isinstance(value, Integer):
        return {'name': 'INTEGER'}
    if isinstance(value, Float):
        return {'name': 'FLOAT'}
    if isinstance(value, Boolean):
        return {'name': 'BOOLEAN'}


def parse_type(value: Any) -> Type:
    name = value['name']

    if name == 'STRING':
        return String()
    if name == 'INTEGER':
        return Integer()
    if name == 'FLOAT':
        return Float()
    if name == 'BOOLEAN':
        return Boolean()
    if name in {'ARRAY', 'DICTIONARY', 'FUNCTION'}:
        value_type = value['value_type']

        if name == 'ARRAY':
            return Array(
                value_type=parse_type(value_type)
            )
        if name == 'DICTIONARY':
            return Dictionary(
                value_type=parse_type(value_type)
            )
        if name == 'FUNCTION':
            return Function(
                value_type=parse_type(value_type)
            )
    if name == 'STRUCT':
        if 'fields' not in value:
            return Struct(fields={})

        return Struct(
            fields={
                Identifier(field): parse_type(subtype)
                for field, subtype in value['fields'].items()
            }
        )
