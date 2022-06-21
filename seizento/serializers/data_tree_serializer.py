from typing import Dict

from seizento.path import Path, EMPTY_PATH
from seizento.serializers.path_serializer import serialize_component, parse_component
from seizento.data_tree import DataTree


def serialize_data_tree(value: DataTree) -> Dict:
    return {
        **value.root_data,
        'children': {
            serialize_component(path_component): serialize_data_tree(subtree)
            for path_component, subtree in value.subtrees.items()
        }

    }


def parse_data_tree(value: Dict) -> DataTree:
    data = {k: v for k, v in value.items() if k != 'children'}
    children = value.get('children') or {}
    result = DataTree(
        values={EMPTY_PATH: data}
    )

    for component, child_value in children.items():
        result = result.add_tree(
            path=Path(components=(parse_component(component),)),
            data_tree=parse_data_tree(child_value)
        )

    return result
