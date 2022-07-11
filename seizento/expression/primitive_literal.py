from __future__ import annotations
from dataclasses import dataclass
from typing import Union, Dict, Set, TYPE_CHECKING

from seizento.identifier import Identifier
from seizento.schema.new_schema import NewSchema, ProperSchema, DataType

from seizento.expression.expression import Expression, ArgumentSpace
from seizento.path import Path, PathComponent


if TYPE_CHECKING:
    from seizento.expression.path_service import PathService


@dataclass(frozen=True)
class PrimitiveLiteral(Expression):
    value: Union[str, int, float, bool, None]

    async def get_schema(self, path_service: PathService) -> NewSchema:
        if isinstance(self.value, str):
            return ProperSchema(types={DataType.STRING})
        if isinstance(self.value, bool):
            return ProperSchema(types={DataType.BOOL})
        if isinstance(self.value, int):
            return ProperSchema(types={DataType.INTEGER})
        if isinstance(self.value, float):
            return ProperSchema(types={DataType.FLOAT})
        if self.value is None:
            return ProperSchema(types={DataType.NULL})

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

    def supports_child_at(self, component: PathComponent) -> bool:
        return False
