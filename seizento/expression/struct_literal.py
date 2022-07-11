from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Set, TYPE_CHECKING

from seizento.data_tree import DataTree
from seizento.identifier import Identifier
from seizento.schema.new_schema import NewSchema, ProperSchema, DataType
from seizento.schema.struct import Struct, EmptyStruct
from seizento.expression.expression import Expression, ArgumentSpace
from seizento.path import Path, PathComponent, LiteralComponent
from seizento.schema.schema import Schema

if TYPE_CHECKING:
    from seizento.expression.path_service import PathService


@dataclass(frozen=True)
class StructLiteral(Expression):
    values: Dict[str, Expression]

    async def get_schema(self, path_service: PathService) -> NewSchema:

        return ProperSchema(
            types={DataType.OBJECT},
            properties={
                prop: await expression.get_schema(path_service)
                for prop, expression in self.values.items()
            }
        )

    async def get_argument_space(
        self,
        path_service: PathService
    ) -> ArgumentSpace:
        result = ArgumentSpace(values={})
        for value in self.values.values():
            result = result.intersect(await value.get_argument_space(path_service=path_service))

        return result

    async def evaluate(
        self,
        path_service: PathService,
        arguments: Dict[Identifier, str]
    ):
        return {
            key: await value.evaluate(path_service, arguments)
            for key, value in self.values.items()
        }

    def supports_child_at(self, component: PathComponent) -> bool:
        return isinstance(component, LiteralComponent)
