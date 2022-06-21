from typing import Any

from seizento.domain.identifier import Identifier
from seizento.domain.types.type import Type
from seizento.domain.types.struct import Struct
from seizento.domain.types.array import Array
from seizento.domain.types.dictionary import Dictionary
from seizento.domain.types.function import Function
from seizento.domain.types.primitives import String, Boolean, Integer, Float


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


def serialize_type(value: Type) -> Any:
    result = {
        'name': NAMES[type(value)]
    }

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


def parse_type(value: Any) -> Type:
    name = value['name']

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
                value_type=parse_type(value_type)
            )
        if name == NAMES[Dictionary]:
            return Dictionary(
                value_type=parse_type(value_type)
            )
        if name == NAMES[Function]:
            return Function(
                value_type=parse_type(value_type)
            )
    if name == NAMES[Struct]:
        if 'fields' not in value:
            return Struct(fields={})

        return Struct(
            fields={
                Identifier(field): parse_type(subtype)
                for field, subtype in value['fields'].items()
            }
        )
