from abc import ABC, abstractmethod

from seizento.domain.expression import Expression
from seizento.domain.path import Path
from seizento.domain.types.type import Type


class Repository(ABC):
    @abstractmethod
    async def get_type(self, path: Path) -> Type:
        pass

    @abstractmethod
    async def set_type(self, path: Path, value: Type) -> None:
        pass

    @abstractmethod
    async def get_expression(self, path: Path) -> Expression:
        pass

    @abstractmethod
    async def set_expression(self, path: Path, value: Expression) -> None:
        pass
