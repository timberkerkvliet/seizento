from typing import Dict

from seizento.domain.type import String, Type, Array, Function, Dictionary, Integer, Float, Boolean, Struct, Identifier


def parse_type(value: Dict, secret_default=False) -> Type:
    if 'name' not in value:
        raise ValueError('Name property expected')
    name = value['name']

    secret = value.get('secret', secret_default)

    if name == 'STRING':
        return String(
            secret=secret,
            optional=value.get('optional', False),
            default_value=value.get('default_value', None)
        )
    if name == 'INTEGER':
        return Integer(
            secret=secret,
            optional=value.get('optional', False),
            default_value=value.get('default_value', None)
        )
    if name == 'FLOAT':
        return Float(
            secret=secret,
            optional=value.get('optional', False),
            default_value=value.get('default_value', None)
        )
    if name == 'BOOLEAN':
        return Boolean(
            secret=secret,
            optional=value.get('optional', False),
            default_value=value.get('default_value', None)
        )
    if name in {'ARRAY', 'DICTIONARY', 'FUNCTION'}:
        if 'value_type' not in value:
            raise ValueError('Missing value type')

        value_type = value['value_type']

        if not isinstance(value_type, dict):
            raise ValueError('Value type is not an object')

        if name == 'ARRAY':
            return Array(
                secret=value.get('secret', False),
                optional=value.get('optional', False),
                value_type=parse_type(value_type, secret_default=secret)
            )
        if name == 'DICTIONARY':
            return Dictionary(
                secret=value.get('secret', False),
                optional=value.get('optional', False),
                value_type=parse_type(value_type, secret_default=secret)
            )
        if name == 'FUNCTION':
            return Function(
                secret=value.get('secret', False),
                optional=value.get('optional', False),
                value_type=parse_type(value_type, secret_default=secret)
            )
    if name == 'STRUCT':
        if 'fields' not in value:
            raise ValueError('Missing fields')
        fields = value['fields']

        if not isinstance(fields, dict):
            raise ValueError('Fields is not an object')

        return Struct(
            secret=value.get('secret', False),
            optional=value.get('optional', False),
            fields={
                Identifier(field): parse_type(field_type, secret_default=secret)
                for field, field_type in fields.items()
            }
        )


parsed = parse_type(
    {
        'name': 'FUNCTION',
        'value_type': {
            'name': 'FUNCTION',
            'value_type': {
                'name': 'STRING'
            }
        }
    }
)
