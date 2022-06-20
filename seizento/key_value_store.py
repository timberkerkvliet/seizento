from abc import abstractmethod
from contextlib import AbstractAsyncContextManager
from pathlib import Path
from typing import Dict, Any


class PathValueStoreTransaction(AbstractAsyncContextManager):
    @abstractmethod
    async def get(self, path: Path) -> Any:
        ...

    @abstractmethod
    async def set(self, path: Path, value: Any) -> None:
        ...

    @abstractmethod
    async def delete(self, path: Path) -> None:
        ...

    @abstractmethod
    async def find_sub_paths(self, path: Path) -> Dict[Path, Any]:
        ...
