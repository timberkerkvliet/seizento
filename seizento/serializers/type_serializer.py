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
        try:
            default_value = value.default_value
        except ValueError:
            default_value = None

        return {
            'name': 'STRING',
            'default_value': default_value,
            'optional': value.is_optional
        }
    if isinstance(value, EncryptedString):
        return {
            'name': 'ENCRYPTED_STRING',
            'optional': value.is_optional
        }
    if isinstance(value, Integer):
        try:
            default_value = value.default_value
        except ValueError:
            default_value = None
        return {
            'name': 'INTEGER',
            'default_value': default_value,
            'optional': value.is_optional
        }
    if isinstance(value, Float):
        try:
            default_value = value.default_value
        except ValueError:
            default_value = None
        return {
            'name': 'FLOAT',
            'default_value': default_value,
            'optional': value.is_optional
        }
    if isinstance(value, Boolean):
        try:
            default_value = value.default_value
        except ValueError:
            default_value = None
        return {
            'name': 'BOOLEAN',
            'default_value': default_value
        }


def parse_type(value: Dict) -> Type:
    if 'name' not in value:
        raise ValueError('Name property expected')
    name = value['name']

    if name == 'STRING':
        return String(
            optional=value.get('optional', False),
            default_value=value.get('default_value', None)
        )
    if name == 'INTEGER':
        return Integer(
            optional=value.get('optional', False),
            default_value=value.get('default_value', None)
        )
    if name == 'FLOAT':
        return Float(
            optional=value.get('optional', False),
            default_value=value.get('default_value', None)
        )
    if name == 'BOOLEAN':
        return Boolean(
            default_value=value.get('default_value', None)
        )
    if name in {'ARRAY', 'DICTIONARY', 'FUNCTION'}:
        if '/~' not in value:
            raise ValueError('Missing value type')

        value_type = value['value_type']

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
