from typing import Any

from seizento.identifier import Identifier
from seizento.schema.new_schema import NewSchema, DataType, ProperSchema, EmptySchema
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


def serialize_schema(value: NewSchema) -> Any:
    result = {}

    if len(value.get_types()) == 1:
        result['type'] = value.get_types().pop().value

    if len(value.get_types()) > 1:
        result['type'] = [data_type.value for data_type in value.types]

    if len(value.get_properties()) > 0:
        result['properties'] = {
            prop: serialize_schema(schema)
            for prop, schema in value.get_properties().items()
        }

    if not value.get_items().empty:
        result['items'] = serialize_schema(value.get_items())

    if not value.get_additional_properties().empty:
        result['additionalProperties'] = serialize_schema(value.get_additional_properties())

    return result


def parse_schema(value: Any) -> NewSchema:
    if 'type' not in value:
        types = set()
    elif isinstance(value['type'], list):
        types = {DataType(val) for val in value['type']}
    else:
        types = {DataType(value['type'])}

    return ProperSchema(
        types=types,
        additional_properties=parse_schema(value['additionalProperties'])
        if 'additionalProperties' in value else EmptySchema(),
        properties={
            prop: parse_schema(val)
            for prop, val in value['properties'].items()
        } if 'properties' in value else {},
        items=parse_schema(value['items']) if 'items' in value else EmptySchema()
    )
