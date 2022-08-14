from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


class PathComponent:
    pass


@dataclass(frozen=True)
class LiteralComponent(PathComponent):
    value: str

    def __post_init__(self):
        if len(self.value) == 0:
            raise ValueError


@dataclass(frozen=True)
class IndexPlaceHolder(PathComponent):
    pass


@dataclass(frozen=True)
class PropertyPlaceHolder(PathComponent):
    pass


@dataclass(frozen=True)
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
    def first_component(self) -> PathComponent:
        return self.components[0]

    @property
    def last_component(self) -> PathComponent:
        return self.components[-1]

    def remove_first(self) -> Path:
        return Path(components=self.components[1:])

    def remove_last(self) -> Path:
        return Path(components=self.components[:-1])

    def __ge__(self, other: Path) -> bool:
        if len(self) < len(other):
            return False

        return self.components[:len(other)] == other.components


EMPTY_PATH = Path(components=tuple())
