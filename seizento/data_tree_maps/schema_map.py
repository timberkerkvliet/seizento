
from seizento.path import LiteralComponent, PropertyPlaceHolder, IndexPlaceHolder
from seizento.schema.schema import Schema, NotAllowed, EverythingAllowed, DataType, Constraint

from seizento.data_tree import DataTree


def constraint_to_tree(value: Constraint) -> DataTree:
    if value == NotAllowed:
        return DataTree(root_data=False)
    if value == EverythingAllowed:
        return DataTree(root_data=True)

    assert isinstance(value, Schema)

    subtrees = {
        LiteralComponent(field): constraint_to_tree(field_type)
        for field, field_type in value.properties.items()
        if not field_type.is_empty()
    }

    additional_properties = value.additional_properties
    if not additional_properties.is_empty():
        subtrees[PropertyPlaceHolder()] = constraint_to_tree(additional_properties)

    items = value.items
    if not items.is_empty():
        subtrees[IndexPlaceHolder()] = constraint_to_tree(items)

    return DataTree(
        root_data={'type': [data_type.value for data_type in value.types]},
        subtrees=subtrees
    )


def tree_to_constraint(value: DataTree) -> Constraint:
    root_data = value.root_data

    if root_data is False:
        return NotAllowed()

    if root_data is True:
        return EverythingAllowed()

    subtrees = value.subtrees
    return Schema(
        types={DataType(val) for val in root_data['type']},
        properties={
            component.value: tree_to_constraint(subtree)
            for component, subtree in subtrees.items()
            if isinstance(component, LiteralComponent)
        },
        additional_properties=tree_to_constraint(subtrees[PropertyPlaceHolder()])
        if PropertyPlaceHolder() in subtrees else EverythingAllowed(),
        items=tree_to_constraint(subtrees[IndexPlaceHolder()])
        if IndexPlaceHolder() in subtrees else EverythingAllowed()
    )
