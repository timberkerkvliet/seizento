from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple, TYPE_CHECKING

from seizento.identifier import Identifier

from seizento.expression.expression import Expression, ArgumentSpace
from seizento.path import PathComponent, LiteralComponent
from seizento.schema.schema import Schema, DataType, Schema, NotAllowed, EverythingAllowed


if TYPE_CHECKING:
    from seizento.expression.path_service import PathService


@dataclass(frozen=True)
class ArrayLiteral(Expression):
    values: Tuple[Expression, ...]

    async def get_schema(self, path_service: PathService) -> Schema:
        schemas = [
            await value.get_schema(path_service) for value in self.values
        ]
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

    def supports_child_at(self, component: PathComponent) -> bool:
        if not isinstance(component, LiteralComponent):
            return False

        return component.value in {str(k) for k in range(len(self.values) + 1)}
