from __future__ import annotations

from dataclasses import dataclass
from typing import Set, TYPE_CHECKING, Union

from seizento.data_tree import DataTree
from seizento.expression.expression import Expression, ArgumentSpace
from seizento.identifier import Identifier
from seizento.path import Path, PathComponent, LiteralComponent, EMPTY_PATH
from seizento.schema.schema import Schema, Schema
from seizento.schema.types import DataType

if TYPE_CHECKING:
    from seizento.expression.path_service import PathService


@dataclass
class ParameterReference(Expression):
    reference: Identifier

    async def get_schema(self, path_service: PathService) -> Schema:
        return Schema(types={DataType.STRING})

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

    def get_child(self, component: PathComponent) -> None:
        raise KeyError

    def set_child(self, component: PathComponent, expression: Expression) -> None:
        raise ValueError

    def delete_child(self, component: PathComponent) -> None:
        return
