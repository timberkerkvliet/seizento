from __future__ import annotations

from dataclasses import dataclass
from typing import Set, TYPE_CHECKING, Union

from seizento.data_tree import DataTree
from seizento.expression.expression import Expression, ArgumentSpace
from seizento.identifier import Identifier
from seizento.path import Path, PathComponent, LiteralComponent, PlaceHolder, EMPTY_PATH
from seizento.schema.primitives import String
from seizento.schema.schema import Schema

if TYPE_CHECKING:
    from seizento.expression.path_service import PathService


@dataclass(frozen=True)
class ParameterReference(Expression):
    reference: Identifier

    async def get_schema(self, path_service: PathService) -> Schema:
        return String()

    async def get_argument_space(
        self,
        path_service: PathService
    ) -> ArgumentSpace:
        return ArgumentSpace(values={})

    async def evaluate(
        self,
        path_service: PathService,
        arguments: dict[Identifier, str]
    ):
        return arguments[self.reference]

    def supports_child_at(self, component: PathComponent) -> bool:
        return False

    def to_tree(self) -> DataTree:
        return DataTree(root_data=self)
