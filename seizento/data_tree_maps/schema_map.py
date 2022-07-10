from seizento.identifier import Identifier
from seizento.path import Path, LiteralComponent, PlaceHolder
from seizento.schema.schema import Schema
from seizento.schema.struct import Struct
from seizento.schema.array import Array
from seizento.schema.dictionary import Dictionary
from seizento.schema.primitives import String, Boolean, Integer, Float, Null
from seizento.data_tree import DataTree


NAMES = {
    Struct: 'STRUCT',
    Dictionary: 'DICTIONARY',
    Array: 'ARRAY',
    String: 'STRING',
    Integer: 'INTEGER',
    Float: 'FLOAT',
    Boolean: 'BOOLEAN',
    Null: 'NULL'
}


def schema_to_tree(value: Schema) -> DataTree:
    if isinstance(value, Struct):
        return DataTree(
            root_data={'type': NAMES[type(value)]},
            subtrees={
                LiteralComponent(field): schema_to_tree(field_type)
                for field, field_type in value.fields.items()
            }
        )

    if isinstance(value, (Array, Dictionary)):
        return DataTree(
            root_data={'type': NAMES[type(value)]},
            subtrees={
                PlaceHolder(): schema_to_tree(value.value_type)
            }
        )

    if isinstance(value, String):
        return DataTree(
            root_data={'type': 'OPTIONAL_STRING' if value.optional else 'STRING'}
        )

    if isinstance(value, Boolean):
        return DataTree(
            root_data={'type': 'OPTIONAL_BOOLEAN' if value.optional else 'BOOLEAN'}
        )

    if isinstance(value, Float):
        return DataTree(
            root_data={'type': 'OPTIONAL_FLOAT' if value.optional else 'FLOAT'}
        )

    if isinstance(value, Integer):
        return DataTree(
            root_data={'type': 'OPTIONAL_INTEGER' if value.optional else 'INTEGER'}
        )

    return DataTree(root_data={'type': NAMES[type(value)]})


def tree_to_schema(value: DataTree) -> Schema:
    root_data = value.root_data

    name = root_data['type']

    if name == 'STRING':
        return String()
    if name == 'OPTIONAL_STRING':
        return String(optional=True)
    if name == 'OPTIONAL_BOOLEAN':
        return Boolean(optional=True)
    if name == 'OPTIONAL_FLOAT':
        return Float(optional=True)
    if name == 'OPTIONAL_INTEGER':
        return Integer(optional=True)
    if name == 'INTEGER':
        return Integer()
    if name == 'FLOAT':
        return Float()
    if name == 'BOOLEAN':
        return Boolean()
    if name == 'NULL':
        return Null()
    if name in {'ARRAY', 'DICTIONARY'}:
        value_type = value.get_subtree(Path(components=(PlaceHolder(),)))

        if name == 'ARRAY':
            return Array(
                value_type=tree_to_schema(value_type)
            )
        if name == 'DICTIONARY':
            return Dictionary(
                value_type=tree_to_schema(value_type)
            )

    if name == 'STRUCT':
        subtrees = value.subtrees

        return Struct(
            fields={
                component.value: tree_to_schema(subtree)
                for component, subtree in subtrees.items()
            }
        )

    raise TypeError
