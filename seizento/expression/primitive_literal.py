from __future__ import annotations
from dataclasses import dataclass
from typing import Union, Dict, Set, TYPE_CHECKING

from seizento.identifier import Identifier
from seizento.schema.schema import Schema
from seizento.schema.types import DataType

from seizento.expression.expression import Expression, ArgumentSpace
from seizento.path import Path, PathComponent


if TYPE_CHECKING:
    from seizento.expression.path_service import PathService


@dataclass(frozen=True)
class PrimitiveLiteral(Expression):
    value: Union[str, int, float, bool, None]

    async def get_schema(self, path_service: PathService) -> Schema:
        if isinstance(self.value, str):
            return Schema(types={DataType.STRING})
        if isinstance(self.value, bool):
            return Schema(types={DataType.BOOL})
        if isinstance(self.value, int):
            return Schema(types={DataType.INTEGER})
        if isinstance(self.value, float):
            return Schema(types={DataType.FLOAT})
        if self.value is None:
            return Schema(types={DataType.NULL})

    async def get_argument_space(
        self,
        path_service: PathService
    ) -> ArgumentSpace:
        return ArgumentSpace(values={})

    async def evaluate(
        self,
        path_service: PathService,
        arguments: Dict[Identifier, str]
    ):
        return self.value

    def get_child(self, component: PathComponent) -> None:
        raise KeyError

    def set_child(self, component: PathComponent, expression: Expression) -> None:
        raise NotImplementedError

    def delete_child(self, component: PathComponent) -> None:
        raise NotImplementedError

