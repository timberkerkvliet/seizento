from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


class Constraint(ABC):
    @abstractmethod
    def satisfies(self, other: Constraint):
        ...

    @abstractmethod
    def union(self, other: Constraint) -> Constraint:
        ...

    @abstractmethod
    def is_empty(self) -> bool:
        ...


@dataclass(frozen=True)
class EverythingAllowed(Constraint):
    def satisfies(self, other: Constraint):
        return other.is_empty()

    def union(self, other: Constraint):
        return self

    def is_empty(self) -> bool:
        return True


@dataclass(frozen=True)
class NotAllowed(Constraint):
    def satisfies(self, other: Constraint):
        return True

    def union(self, other: Constraint) -> Constraint:
        return other

    def is_empty(self) -> bool:
        return False
