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

    async def get_schema(self, path_service: PathService) -> Schema:
        return Schema(
            types={DataType.OBJECT},
            additional_properties=await self.value.get_schema(path_service)
        )

    async def _internal_space(self, path_service: PathService) -> ArgumentSpace:
        key_space = await self.key.get_argument_space(path_service=path_service)
        value_space = await self.value.get_argument_space(path_service=path_service)

        return key_space.intersect(value_space)

    async def get_argument_space(
        self,
        path_service: PathService
    ) -> ArgumentSpace:
        return (await self._internal_space(path_service)).remove(self.parameter)

    async def evaluate(self, path_service: PathService, arguments: Dict[Identifier, str]) -> Any:
        argument_space = await self._internal_space(path_service)

        if self.parameter not in argument_space:
            raise Exception

        return {
            await self.key.evaluate(path_service=path_service, arguments={**arguments, self.parameter: value}):
                await self.value.evaluate(path_service=path_service, arguments={**arguments, self.parameter: value})
            for value in argument_space.values[self.parameter]
        }

    def get_child(self, component: PathComponent) -> Expression:
        if component == PropertyPlaceHolder():
            return self.value

    def set_child(self, component: PathComponent, expression: Expression) -> None:
        if component == PropertyPlaceHolder():
            self.value = expression

    def delete_child(self, component: PathComponent) -> None:
        raise NotImplementedError
