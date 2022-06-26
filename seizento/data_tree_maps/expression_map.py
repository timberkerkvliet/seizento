from seizento.data_tree import DataTree
from seizento.expression.expression import Expression
from seizento.expression.primitive_literal import PrimitiveLiteral
from seizento.expression.array_literal import ArrayLiteral
from seizento.expression.struct_literal import StructLiteral
from seizento.expression.path_reference import PathReference
from seizento.path import EMPTY_PATH, Path, StringComponent
from seizento.serializers.path_serializer import serialize_path, parse_path


def expression_to_tree(value: Expression) -> DataTree:
    if isinstance(value, PrimitiveLiteral):
        return DataTree.from_subtrees(root_data=value.value)

    if isinstance(value, StructLiteral):
        return DataTree.from_subtrees(
            root_data={'type': 'OBJECT'},
            subtrees={
                StringComponent(str(name)): expression_to_tree(expression)
                for name, expression in value.values.items()
            }
        )

    if isinstance(value, ArrayLiteral):
        return DataTree.from_subtrees(
            root_data={'type': 'ARRAY'},
            subtrees={
                StringComponent(str(k)): expression_to_tree(child)
                for k, child in enumerate(value.values)
            }
        )

    if isinstance(value, PathReference):
        return DataTree.from_subtrees(
            root_data={'type': 'PATH_REFERENCE', 'reference': serialize_path(value.reference)}
        )

    raise TypeError(type(value))


def tree_to_expression(value: DataTree) -> Expression:
    root_data = value.root_data
    if isinstance(root_data, dict) and root_data.get('type') == 'ARRAY':
        subtrees = value.subtrees
        values = {
            component.value: tree_to_expression(subtree)
            for component, subtree in subtrees.items()
        }
        return ArrayLiteral(
            values=tuple(y for _, y in sorted(values.items()))
        )

    if isinstance(root_data, dict) and root_data.get('type') == 'OBJECT':
        subtrees = value.subtrees
        values = {
            component.value: tree_to_expression(subtree)
            for component, subtree in subtrees.items()
        }
        return StructLiteral(
            values=values
        )

    if isinstance(root_data, dict) and root_data.get('type') == 'PATH_REFERENCE':
        reference = parse_path(root_data['reference'])
        return PathReference(reference=reference)

    if isinstance(root_data, int):
        return PrimitiveLiteral(root_data)

    if isinstance(root_data, str):
        return PrimitiveLiteral(root_data)

    raise TypeError
