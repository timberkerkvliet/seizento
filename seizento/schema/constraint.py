from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict

from seizento.path import PathComponent, Path


class Constraint(ABC):
    @abstractmethod
    def satisfies(self, other: Constraint):
        ...

    @abstractmethod
    def union(self, other: Constraint) -> Constraint:
        ...

    @abstractmethod
    def intersection(self, other: Constraint) -> Constraint:
        ...

    @abstractmethod
    def is_empty(self) -> bool:
        ...

    @abstractmethod
    def get_child(self, component: PathComponent) -> Constraint:
        ...

    @abstractmethod
    def set_child(self, component: PathComponent, constraint: Constraint) -> bool:
        ...

    @abstractmethod
    def delete_child(self, component: PathComponent) -> None:
        ...

    def navigate_to(self, path: Path) -> Constraint:
        result = self
        for component in path:
            result = result.get_child(component)

        return result


@dataclass(frozen=True)
class EverythingAllowed(Constraint):
    def satisfies(self, other: Constraint):
        return other.is_empty()

    def union(self, other: Constraint):
        return self

    def intersection(self, other: Constraint) -> Constraint:
        return other

    def is_empty(self) -> bool:
        return True

    def get_child(self, component: PathComponent) -> None:
        raise KeyError

    def set_child(self, component: PathComponent, constraint: Constraint) -> bool:
        raise Exception

    def delete_child(self, component: PathComponent) -> None:
        return


@dataclass(frozen=True)
class NotAllowed(Constraint):
    def satisfies(self, other: Constraint):
        return True

    def union(self, other: Constraint) -> Constraint:
        return other

    def intersection(self, other: Constraint) -> Constraint:
        return self

    def is_empty(self) -> bool:
        return False

    def get_child(self, component: PathComponent) -> None:
        raise KeyError

    def set_child(self, component: PathComponent, constraint: Constraint) -> bool:
        raise Exception

    def delete_child(self, component: PathComponent) -> None:
        return
