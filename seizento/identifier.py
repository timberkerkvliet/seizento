from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Identifier:
    name: str

    def __post_init__(self):
        normalized = self.name.replace('_', '').replace('-', '')
        if not normalized.isalnum() or not normalized.isascii():
            raise ValueError(f'Invalid identifier: {self.name}')

    def __str__(self):
        return self.name
