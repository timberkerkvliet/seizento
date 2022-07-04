from dataclasses import dataclass
from typing import Set
from uuid import UUID

from seizento.path import Path


@dataclass(frozen=True)
class AccessRights:
    read_access: Set[Path]
    write_access: Set[Path]

    def can_read(self, path) -> bool:
        return any(path >= read_path for read_path in self.read_access)

    def can_write(self, path) -> bool:
        return any(path >= write_path for write_path in self.write_access)


@dataclass(frozen=True)
class User:
    id: UUID
    password: str
    access_rights: AccessRights
