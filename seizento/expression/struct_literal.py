from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Set, TYPE_CHECKING

from seizento.data_tree import DataTree
from seizento.identifier import Identifier
from seizento.schema.schema import Schema, Schema
from seizento.schema.constraint import NotAllowed
from seizento.schema.types import DataType

from seizento.expression.expression import Expression, ArgumentSpace
from seizento.path import Path, PathComponent, LiteralComponent


if TYPE_CHECKING:
    from seizento.expression.path_service import PathService


@dataclass
class StructLiteral(Expression):
    values: Dict[str, Expression]

    def get_schema(self, root_schema: Schema) -> Schema:

        return Schema(
            types={DataType.OBJECT},
            properties={
                prop: expression.get_schema(root_schema)
                for prop, expression in self.values.items()
            },
            additional_properties=NotAllowed()
        )

    def get_argument_space(
        self,
        root_expression: Expression
    ) -> ArgumentSpace:
        result = ArgumentSpace(values={})
        for value in self.values.values():
            result = result.intersect(value.get_argument_space(root_expression=root_expression))

        return result

    def evaluate(
        self,
        root_expression: Expression,
        arguments: Dict[Identifier, str]
    ):
        return {
            key: value.evaluate(root_expression, arguments)
            for key, value in self.values.items()
        }

    def get_child(self, component: PathComponent) -> Expression:
        if isinstance(component, LiteralComponent):
            return self.values[component.value]

        raise KeyError

    def set_child(self, component: PathComponent, expression: Expression) -> None:
        if isinstance(component, LiteralComponent):
            self.values[component.value] = expression
            return

        raise ValueError

    def delete_child(self, component: PathComponent) -> None:
        if isinstance(component, LiteralComponent):
            self.values.pop(component.value, None)
