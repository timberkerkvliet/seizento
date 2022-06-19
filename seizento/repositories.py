from abc import ABC, abstractmethod

from seizento.domain.type import Type


class TypeRepository(ABC):
    @abstractmethod
    async def get(self, root: str) -> Type:
        pass

    @abstractmethod
    async def set(self, root: str, type: Type) -> None:
        pass
