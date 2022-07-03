from seizento.data_tree import DataTree
from seizento.expression.expression import Expression
from seizento.expression.parametrized_dictionary import ParametrizedDictionary
from seizento.expression.primitive_literal import PrimitiveLiteral
from seizento.expression.array_literal import ArrayLiteral
from seizento.expression.struct_literal import StructLiteral
from seizento.expression.path_reference import PathReference
from seizento.identifier import Identifier
from seizento.path import EMPTY_PATH, Path, LiteralComponent, PlaceHolder
from seizento.serializers.expression_serializer import serialize_expression, parse_expression
from seizento.serializers.path_serializer import serialize_path, parse_path


def expression_to_tree(value: Expression) -> DataTree:
    if isinstance(value, PrimitiveLiteral):
        return DataTree(root_data=value.value)

    if isinstance(value, StructLiteral):
        return DataTree(
            root_data={'type': 'OBJECT'},
            subtrees={
                LiteralComponent(str(name)): expression_to_tree(expression)
                for name, expression in value.values.items()
            }
        )

    if isinstance(value, ArrayLiteral):
        return DataTree(
            root_data={'type': 'ARRAY'},
            subtrees={
                LiteralComponent(str(k)): expression_to_tree(child)
                for k, child in enumerate(value.values)
            }
        )

    if isinstance(value, PathReference):
        return DataTree(
            root_data={
                'type': 'PATH_REFERENCE',
                'reference': serialize_expression(value)
            }
        )

    if isinstance(value, ParametrizedDictionary):
        return DataTree(
            root_data={
                'type': 'PARAMETRIZED_DICTIONARY',
                'parameter': value.parameter.name,
                'key': serialize_expression(value.key)
            },
            subtrees={
                PlaceHolder(): expression_to_tree(value.value)
            }
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
        ref = root_data['reference']
        return parse_expression(ref)

    if isinstance(root_data, dict) and root_data.get('type') == 'PARAMETRIZED_DICTIONARY':
        return ParametrizedDictionary(
            key=parse_expression(root_data['key']),
            parameter=Identifier(root_data['parameter']),
            value=tree_to_expression(value.subtrees[PlaceHolder()])
        )

    if isinstance(root_data, int):
        return PrimitiveLiteral(root_data)

    if isinstance(root_data, str):
        return PrimitiveLiteral(root_data)

    raise TypeError
