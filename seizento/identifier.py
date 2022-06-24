from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Identifier:
    name: str

    def __post_init__(self):
        if not self.name.replace('_', '').replace('-', '').isalnum():
            raise ValueError(f'Invalid identifier: {self.name}')


