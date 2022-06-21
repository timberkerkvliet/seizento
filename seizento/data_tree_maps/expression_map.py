from seizento.data_tree import DataTree
from seizento.domain.expression import Expression, PrimitiveLiteral, ArrayLiteral
from seizento.path import EMPTY_PATH, Path, StringComponent


def expression_to_tree(value: Expression) -> DataTree:
    if isinstance(value, PrimitiveLiteral):
        return DataTree(values={EMPTY_PATH:  value.value})

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

    if isinstance(root_data, int):
        return PrimitiveLiteral(root_data)

    if isinstance(root_data, str):
        return PrimitiveLiteral(root_data)

    raise TypeError
