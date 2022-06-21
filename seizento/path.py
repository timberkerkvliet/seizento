from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


class PathComponent:
    pass


@dataclass(frozen=True)
class StringComponent(PathComponent):
    value: str


class PlaceHolder(PathComponent):
    pass


@dataclass(frozen=True)
class Path:
    components: Tuple[PathComponent, ...]

    def __len__(self) -> int:
        return len(self.components)

    def __iter__(self):
        return iter(self.components)

    @property
    def empty(self) -> bool:
        return len(self) == 0

    @property
    def first_component(self) -> PathComponent:
        return self.components[0]

    @property
    def last_component(self) -> PathComponent:
        return self.components[-1]

    def remove_from_start(self, n: int) -> Path:
        return Path(components=self.components[n:])

    def remove_first(self) -> Path:
        return Path(components=self.components[1:])

    def remove_last(self) -> Path:
        return Path(components=self.components[:-1])

    def append(self, component: PathComponent) -> Path:
        return Path(components=self.components + (component,))

    def __add__(self, other):
        if not isinstance(other, Path):
            raise TypeError

        return Path(components=self.components + other.components)


EMPTY_PATH = Path(components=tuple())
