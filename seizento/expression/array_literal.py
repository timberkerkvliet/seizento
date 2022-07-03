from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple, TYPE_CHECKING

from seizento.identifier import Identifier
from seizento.schema.array import Array, EmptyArray
from seizento.expression.expression import Expression, ArgumentSpace
from seizento.path import PathComponent, LiteralComponent
from seizento.schema.schema import Schema

if TYPE_CHECKING:
    from seizento.expression.path_service import PathService


@dataclass(frozen=True)
class ArrayLiteral(Expression):
    values: Tuple[Expression, ...]

    async def get_schema(self, path_service: PathService) -> Schema:
        if len(self.values) == 0:
            return EmptyArray()

        schemas = {
            await value.get_schema(path_service) for value in self.values
        }

        if len(schemas) > 1:
            super_schema = schemas.pop()
            for schema in schemas:
                super_schema = super_schema.common_superschema(schema)

            if super_schema is not None:
                return Array(value_type=super_schema)

            raise ValueError('Mixed types')

        return Array(value_type=schemas.pop())

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

    def supports_child_at(self, component: PathComponent) -> bool:
        if not isinstance(component, LiteralComponent):
            return False

        return component.value in {str(k) for k in range(len(self.values) + 1)}
