from typing import Dict

from seizento.domain.identifier import Identifier
from seizento.domain.path import PathComponent
from seizento.domain.types.type import Type
from seizento.domain.types.struct import Struct
from seizento.domain.types.array import Array
from seizento.domain.types.dictionary import Dictionary
from seizento.domain.types.function import Function
from seizento.domain.types.primitives import String, EncryptedString, Boolean, Integer, Float
from seizento.serializers.path_serializer import serialize_component


def serialize_subtypes(subtypes: Dict[PathComponent, Type]):
    return {
        serialize_component(component): serialize_type(subtype)
        for component, subtype in subtypes.items()
    }


def serialize_type(value: Type):
    result = serialize_root_of_type(value)
    subtypes = value.get_subtypes()
    if subtypes is not None:
        result['subtypes'] = serialize_subtypes(subtypes)

    return result


def serialize_root_of_type(value: Type):
    if isinstance(value, Struct):
        return {
            'name': 'STRUCT'
        }
    if isinstance(value, Dictionary):
        return {
            'name': 'DICTIONARY'
        }
    if isinstance(value, Array):
        return {
            'name': 'ARRAY'
        }
    if isinstance(value, Function):
        return {
            'name': 'FUNCTION'
        }
    if isinstance(value, String):
        return {'name': 'STRING'}
    if isinstance(value, EncryptedString):
        return {'name': 'ENCRYPTED_STRING'}
    if isinstance(value, Integer):
        return {'name': 'INTEGER'}
    if isinstance(value, Float):
        return {'name': 'FLOAT'}
    if isinstance(value, Boolean):
        return {'name': 'BOOLEAN'}


def parse_type(value: Dict) -> Type:
    if 'name' not in value:
        raise ValueError('Name property expected')
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
        value_type = value['subtypes']['~']

        if not isinstance(value_type, dict):
            raise ValueError('Value type is not an object')

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
        fields = value['subtypes']

        if not isinstance(fields, dict):
            raise ValueError('Fields is not an object')

        return Struct(
            fields={
                Identifier(field): parse_type(field_type)
                for field, field_type in fields.items()
            }
        )
