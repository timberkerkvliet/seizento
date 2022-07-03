from __future__ import annotations
from dataclasses import dataclass
from typing import Union, Dict, Set, TYPE_CHECKING

from seizento.data_tree import DataTree
from seizento.identifier import Identifier
from seizento.schema.primitives import String, Integer, Boolean
from seizento.expression.expression import Expression, ArgumentSpace
from seizento.path import Path, PathComponent
from seizento.schema.schema import Schema

if TYPE_CHECKING:
    from seizento.expression.path_service import PathService


@dataclass(frozen=True)
class PrimitiveLiteral(Expression):
    value: Union[str, int, float, bool]

    def get_schema(self, schemas: Dict[Path, Schema]) -> Schema:
        if isinstance(self.value, str):
            return String()
        if isinstance(self.value, bool):
            return Boolean()
        if isinstance(self.value, int):
            return Integer()

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

    def get_path_references(self) -> Set[Path]:
        return set()

    def supports_child_at(self, component: PathComponent) -> bool:
        return False

    def to_tree(self) -> DataTree:
        return DataTree(root_data=self.value)
