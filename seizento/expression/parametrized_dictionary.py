from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Set, Any, TYPE_CHECKING

from seizento.data_tree import DataTree
from seizento.identifier import Identifier

from seizento.expression.expression import Expression, ArgumentSpace
from seizento.path import Path, PathComponent, PropertyPlaceHolder
from seizento.schema.schema import Schema
from seizento.schema.types import DataType

if TYPE_CHECKING:
    from seizento.expression.path_service import PathService


@dataclass
class ParametrizedDictionary(Expression):
    parameter: Identifier
    key: Expression
    value: Expression

    def get_schema(self, root_schema: Schema) -> Schema:
        return Schema(
            types={DataType.OBJECT},
            additional_properties=self.value.get_schema(root_schema)
        )

    async def _internal_space(self, root_expression: Expression) -> ArgumentSpace:
        key_space = await self.key.get_argument_space(root_expression=root_expression)
        value_space = await self.value.get_argument_space(root_expression=root_expression)

        return key_space.intersect(value_space)

    async def get_argument_space(
        self,
        root_expression: Expression
    ) -> ArgumentSpace:
        return (await self._internal_space(root_expression)).remove(self.parameter)

    async def evaluate(self, root_expression: Expression, arguments: Dict[Identifier, str]) -> Any:
        argument_space = await self._internal_space(root_expression)

        if self.parameter not in argument_space:
            raise Exception

        return {
            await self.key.evaluate(root_expression=root_expression, arguments={**arguments, self.parameter: value}):
                await self.value.evaluate(root_expression=root_expression, arguments={**arguments, self.parameter: value})
            for value in argument_space.values[self.parameter]
        }

    def get_child(self, component: PathComponent) -> Expression:
        if component == PropertyPlaceHolder():
            return self.value

    def set_child(self, component: PathComponent, expression: Expression) -> None:
        if component == PropertyPlaceHolder():
            self.value = expression
            return

        raise ValueError

    def delete_child(self, component: PathComponent) -> None:
        raise NotImplementedError
