from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List
from urllib.parse import quote, unquote


class PathComponent(ABC):
    @abstractmethod
    def serialize(self) -> str:
        """Serializes to """


@dataclass(frozen=True)
class PathValue(PathComponent):
    value: str

    def serialize(self) -> str:
        return quote(self.value)


class PlaceHolder(PathComponent):
    def serialize(self) -> str:
        return '~'


@dataclass(frozen=True)
class Path:
    components: List[PathComponent]

    def serialize(self) -> str:
        return '/'.join([component.serialize() for component in self.components])

    def __len__(self) -> int:
        return len(self.components)

    @property
    def empty(self) -> bool:
        return len(self) == 0

    @property
    def first_component(self) -> PathComponent:
        return self.components[0]

    def remove_first_component(self) -> Path:
        return Path(components=self.components[1:])

    def remove_last_component(self) -> Path:
        return Path(components=self.components[:-1])
