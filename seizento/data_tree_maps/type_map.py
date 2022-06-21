from seizento.domain.identifier import Identifier
from seizento.path import Path, StringComponent, PlaceHolder
from seizento.domain.types.type import Type
from seizento.domain.types.struct import Struct
from seizento.domain.types.array import Array
from seizento.domain.types.dictionary import Dictionary
from seizento.domain.types.function import Function
from seizento.domain.types.primitives import String, Boolean, Integer, Float
from seizento.data_tree import DataTree


def type_to_tree(value: Type) -> DataTree:
    result = DataTree(
        values={
            Path(components=tuple()): serialize_root_data(value)
        }
    )

    if isinstance(value, Struct):
        for field, field_type in value.fields.items():
            result = result.set_subtree(
                path=Path(components=(StringComponent(field.name),)),
                subtree=type_to_tree(field_type)
            )

    if isinstance(value, (Array, Function, Dictionary)):
        result = result.set_subtree(
            path=Path(components=(PlaceHolder(),)),
            subtree=type_to_tree(value.value_type)
        )

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


def tree_to_type(value: DataTree) -> Type:
    root_data = value.root_data
    if 'name' not in root_data:
        raise ValueError('Name property expected')
    name = root_data['name']

    if name == 'STRING':
        return String()
    if name == 'INTEGER':
        return Integer()
    if name == 'FLOAT':
        return Float()
    if name == 'BOOLEAN':
        return Boolean()
    if name in {'ARRAY', 'DICTIONARY', 'FUNCTION'}:
        value_type = value.get_subtree(Path(components=(PlaceHolder(),)))

        if name == 'ARRAY':
            return Array(
                value_type=tree_to_type(value_type)
            )
        if name == 'DICTIONARY':
            return Dictionary(
                value_type=tree_to_type(value_type)
            )
        if name == 'FUNCTION':
            return Function(
                value_type=tree_to_type(value_type)
            )
    if name == 'STRUCT':
        subtrees = value.subtrees

        return Struct(
            fields={
                Identifier(component.value): tree_to_type(subtree)
                for component, subtree in subtrees.items()
            }
        )
