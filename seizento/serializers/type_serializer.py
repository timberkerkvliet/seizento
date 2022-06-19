from seizento.domain.type import Type, Struct, Dictionary, Array, Float, Function, String, EncryptedString, Boolean


def serialize_type(value: Type):
    if isinstance(value, Struct):
        return {
            'name': 'STRUCT',
            'fields': {
                field: serialize_type(field_type)
                for field, field_type in value.fields.items()
            }
        }
    if isinstance(value, Dictionary):
        return {
            'name': 'DICTIONARY',
            'value_type': serialize_type(value.value_type)
        }
    if isinstance(value, Array):
        return {
            'name': 'ARRAY',
            'value_type': serialize_type(value.value_type)
        }
    if isinstance(value, Function):
        return {
            'name': 'FUNCTION',
            'value_type': serialize_type(value.value_type)
        }
    if isinstance(value, String):
        return {
            'name': 'STRING',
            'default_value': value.default_value
        }
    if isinstance(value, EncryptedString):
        return {
            'name': 'ENCRYPTED_STRING',
            'optional': value.optional
        }
    if isinstance(value, Float):
        return {
            'name': 'FLOAT',
            'default_value': value.default_value
        }
    if isinstance(value, Boolean):
        return {
            'name': 'BOOLEAN',
            'default_value': value.default_value
        }
