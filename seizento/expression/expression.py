from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Set, Any, TYPE_CHECKING

from seizento.data_tree import DataTree
from seizento.identifier import Identifier
from seizento.path import Path, PathComponent
from seizento.schema.schema import Schema

if TYPE_CHECKING:
    from seizento.expression.path_service import PathService


@dataclass(frozen=True)
class ArgumentSpace:
    values: Dict[Identifier, Set[str]]

    def intersect(self, other: ArgumentSpace) -> ArgumentSpace:
        return ArgumentSpace(
            values={
                **{
                    k: v for k, v in self.values.items()
                    if k not in other.values
                },
                **{
                    k: v for k, v in other.values.items()
                    if k not in self.values
                },
                **{
                    k: v & other.values[k] for k, v in self.values.items()
                    if k in other.values
                }
            }
        )

    def remove(self, parameter: Identifier) -> ArgumentSpace:
        return ArgumentSpace(
            values={k: v for k, v in self.values.items() if k != parameter}
        )

    def __iter__(self):
        return iter(self.values)


class Expression(ABC):
    @abstractmethod
    async def get_schema(self, path_service: PathService) -> Schema:
        pass

    @abstractmethod
    async def get_argument_space(
        self,
        path_service: PathService
    ) -> ArgumentSpace:
        pass

    @abstractmethod
    async def evaluate(
        self,
        path_service: PathService,
        arguments: Dict[Identifier, str]
    ) -> Any:
        pass

    @abstractmethod
    def get_path_references(self) -> Set[Path]:
        pass

    @abstractmethod
    def supports_child_at(self, component: PathComponent) -> bool:
        pass

    @abstractmethod
    def to_tree(self) -> DataTree:
        pass
