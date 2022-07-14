from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple, TYPE_CHECKING, List

from seizento.identifier import Identifier

from seizento.expression.expression import Expression, ArgumentSpace
from seizento.path import PathComponent, LiteralComponent
from seizento.schema.schema import Schema, Schema
from seizento.schema.constraint import EverythingAllowed, NotAllowed
from seizento.schema.types import DataType


@dataclass
class ArrayLiteral(Expression):
    values: List[Expression, ...]

    def get_schema(self, root_schema: Schema) -> Schema:
        schemas = [value.get_schema(root_schema) for value in self.values]
        item_schema = NotAllowed()
        for schema in schemas:
            item_schema = item_schema.union(schema)

        return Schema(
            types={DataType.ARRAY},
            items=item_schema
        )

    def get_argument_space(
        self,
        root_expression: Expression,
    ) -> ArgumentSpace:
        result = ArgumentSpace(values={})
        for value in self.values:
            result = result.intersect(value.get_argument_space(root_expression=root_expression))

        return result

    def evaluate(
        self,
        root_expression: Expression,
        arguments: Dict[Identifier, str]
    ):
        return [value.evaluate(root_expression, arguments) for value in self.values]

    def get_child(self, component: PathComponent) -> Expression:
        if isinstance(component, LiteralComponent):
            index = int(component.value)

            if index >= len(self.values):
                raise KeyError

            return self.values[index]

    def set_child(self, component: PathComponent, expression: Expression) -> None:
        if not isinstance(component, LiteralComponent):
            raise ValueError

        index = int(component.value)

        if index < len(self.values):
            self.values[index] = expression
            return
        if index == len(self.values):
            self.values.append(expression)
            return

        raise ValueError

    def delete_child(self, component: PathComponent) -> None:
        return
