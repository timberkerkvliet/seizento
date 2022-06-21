from typing import Dict, Any

from seizento.path import Path, EMPTY_PATH
from seizento.serializers.path_serializer import serialize_component, parse_component
from seizento.data_tree import DataTree


def serialize_data_tree(value: DataTree) -> Dict:
    subtrees = value.subtrees
    if len(subtrees) == 0:
        return value.root_data

    return {
        **value.root_data,
        'children': {
            serialize_component(path_component): serialize_data_tree(subtree)
            for path_component, subtree in subtrees.items()
        }

    }


def parse_data_tree(value: Any) -> DataTree:
    if not isinstance(value, dict):
        return DataTree(values={EMPTY_PATH: value})
    
    data = {k: v for k, v in value.items() if k != 'children'}
    children = value.get('children') or {}
    result = DataTree(
        values={EMPTY_PATH: data}
    )

    for component, child_value in children.items():
        result = result.set_subtree(
            path=Path(components=(parse_component(component),)),
            subtree=parse_data_tree(child_value)
        )

    return result
