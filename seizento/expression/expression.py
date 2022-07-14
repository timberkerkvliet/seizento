from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Set, Any, TYPE_CHECKING

from seizento.identifier import Identifier
from seizento.path import PathComponent
from seizento.schema.schema import Schema

if TYPE_CHECKING:
    from seizento.expression.path_service import PathService


@dataclass(frozen=True)
class ArgumentSpace:
    values: Dict[Identifier, Set[str]]

    def intersect(self, other: ArgumentSpace) -> ArgumentSpace:
        return ArgumentSpace(
            values={
                **self.values,
                **other.values,
                **{
                    k: self.values[k] & other.values[k]
                    for k in set(self.values) & set(other.values)
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
    def get_schema(self, root_schema: Schema) -> Schema:
        pass

    @abstractmethod
    async def get_argument_space(
        self,
        root_expression: Expression
    ) -> ArgumentSpace:
        pass

    @abstractmethod
    async def evaluate(
        self,
        root_expression: Expression,
        arguments: Dict[Identifier, str]
    ) -> Any:
        pass

    @abstractmethod
    def get_child(self, component: PathComponent) -> None:
        pass

    @abstractmethod
    def set_child(self, component: PathComponent, expression: Expression) -> None:
        pass

    @abstractmethod
    def delete_child(self, component: PathComponent) -> None:
        pass
