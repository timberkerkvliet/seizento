from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple, TYPE_CHECKING, List

from seizento.identifier import Identifier

from seizento.expression.expression import Expression, ArgumentSpace
from seizento.path import PathComponent, LiteralComponent
from seizento.schema.schema import Schema, Schema
from seizento.schema.constraint import EverythingAllowed, NotAllowed
from seizento.schema.types import DataType

if TYPE_CHECKING:
    from seizento.expression.path_service import PathService


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

    async def get_argument_space(
        self,
        path_service: PathService
    ) -> ArgumentSpace:
        result = ArgumentSpace(values={})
        for value in self.values:
            result = result.intersect(await value.get_argument_space(path_service=path_service))

        return result

    async def evaluate(
        self,
        path_service: PathService,
        arguments: Dict[Identifier, str]
    ):
        return [await value.evaluate(path_service, arguments) for value in self.values]

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
