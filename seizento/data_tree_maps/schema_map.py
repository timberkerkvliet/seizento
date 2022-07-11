from seizento.identifier import Identifier
from seizento.path import Path, LiteralComponent, PropertyPlaceHolder, IndexPlaceHolder
from seizento.schema.new_schema import NewSchema, EmptySchema, ProperSchema, DataType
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


def schema_to_tree(value: NewSchema) -> DataTree:
    subtrees = {
        LiteralComponent(field): schema_to_tree(field_type)
        for field, field_type in value.get_properties().items()
    }

    if not value.get_additional_properties().empty:
        subtrees[PropertyPlaceHolder()] = schema_to_tree(value.get_additional_properties())

    if not value.get_items().empty:
        subtrees[IndexPlaceHolder()] = schema_to_tree(value.get_items())

    return DataTree(
        root_data={
            'type': [data_type.value for data_type in value.get_types()]
        },
        subtrees=subtrees
    )


def tree_to_schema(value: DataTree) -> NewSchema:
    root_data = value.root_data
    subtrees = value.subtrees
    return ProperSchema(
        types={DataType(val) for val in root_data['type']},
        properties={
            component.value: tree_to_schema(subtree)
            for component, subtree in subtrees.items()
            if isinstance(component, LiteralComponent)
        },
        additional_properties=tree_to_schema(subtrees[PropertyPlaceHolder()])
        if PropertyPlaceHolder() in subtrees else EmptySchema(),
        items=tree_to_schema(subtrees[IndexPlaceHolder()])
        if IndexPlaceHolder() in subtrees else EmptySchema()
    )
