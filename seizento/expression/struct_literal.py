from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Set, TYPE_CHECKING

from seizento.data_tree import DataTree
from seizento.identifier import Identifier
from seizento.schema.struct import Struct, EmptyStruct
from seizento.expression.expression import Expression, ArgumentSpace
from seizento.path import Path, PathComponent, LiteralComponent
from seizento.schema.schema import Schema

if TYPE_CHECKING:
    from seizento.expression.path_service import PathService


@dataclass(frozen=True)
class StructLiteral(Expression):
    values: Dict[str, Expression]

    def get_schema(self, schemas: Dict[Path, Schema]) -> Schema:
        if len(self.values) == 0:
            return EmptyStruct()

        return Struct(
            fields={Identifier(x): y.get_schema(schemas) for x, y in self.values.items()}
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

    def get_path_references(self) -> Set[Path]:
        return {
            reference for expression in self.values.values()
            for reference in expression.get_path_references()
        }

    def supports_child_at(self, component: PathComponent) -> bool:
        if not isinstance(component, LiteralComponent):
            return False

        return component.value in self.values

    def to_tree(self) -> DataTree:
        return DataTree(
            root_data=self,
            subtrees={
                LiteralComponent(str(name)): expression.to_tree()
                for name, expression in self.values.items()
            }
        )
