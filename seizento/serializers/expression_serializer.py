from seizento.data_tree import DataTree
from seizento.domain.expression import Expression, PrimitiveLiteral
from seizento.path import EMPTY_PATH


def serialize_expression(value: Expression) -> DataTree:
    if isinstance(value, PrimitiveLiteral):
        return DataTree(values={EMPTY_PATH: {'literal': value.value}})

    raise TypeError(type(value))


def parse_expression(value: DataTree) -> Expression:
    return PrimitiveLiteral(value.root_data['literal'])
