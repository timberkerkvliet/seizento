from __future__ import annotations

from dataclasses import dataclass
from typing import List, Union, Dict


@dataclass(frozen=True)
class Identifier:
    name: str

    def __post_init__(self):
        if not self.name.replace('_', '').replace('-', '').isalnum():
            raise ValueError(f'Invalid identifier: {self.name}')

    def __str__(self):
        return self.name


@dataclass(frozen=True)
class NodeIdentifier:
    root: Identifier
    path: List[Identifier]

    def __str__(self) -> str:
        all_ids = [self.root] + self.path
        return '/'.join([identifier.name for identifier in all_ids])

    @classmethod
    def parse_from_string(cls, value: str) -> NodeIdentifier:
        parts = value.split('/')

        return cls(
            root=Identifier(parts[0]),
            path=[Identifier(part) for part in parts[1:]]
        )

    @property
    def path_as_identifier(self) -> NodeIdentifier:
        return NodeIdentifier(
            root=self.path[0],
            path=self.path[1:]
        )
