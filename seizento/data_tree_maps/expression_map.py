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
        return DataTree(values={EMPTY_PATH:  value.value})

    if isinstance(value, StructLiteral):
        result = DataTree(values={EMPTY_PATH: {'type': 'OBJECT'}})
        for name, expression in value.values.items():
            result = result.set_subtree(
                path=Path(components=(StringComponent(str(name)),)),
                subtree=expression_to_tree(expression)
            )

        return result

    if isinstance(value, ArrayLiteral):
        result = DataTree(
            values={
                EMPTY_PATH: {'type': 'ARRAY'}
            }
        )
        for k, child in enumerate(value.values):
            result = result.set_subtree(
                path=Path(components=(StringComponent(str(k)),)),
                subtree=expression_to_tree(child)
            )
        return result

    if isinstance(value, PathReference):
        return DataTree(
            values={EMPTY_PATH: {'type': 'PATH_REFERENCE', 'reference': serialize_path(value.reference)}}
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
