from __future__ import annotations

import base64
from dataclasses import dataclass
from typing import Set, Union

import bcrypt as bcrypt

from seizento.identifier import Identifier
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
class HashedPassword:
    value: bytes

    @classmethod
    def from_password(cls, password: str) -> HashedPassword:
        return cls(
            value=bcrypt.hashpw(password.encode(), salt=bcrypt.gensalt(rounds=5))
        )

    @classmethod
    def from_string(cls, value: str) -> HashedPassword:
        return cls(value=base64.b64decode(value.encode()))

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode(), self.value)

    def __str__(self) -> str:
        return base64.b64encode(self.value).decode()


@dataclass(frozen=True)
class User:
    id: Identifier
    password: HashedPassword
    access_rights: AccessRights

    def with_new_password(self, password: HashedPassword) -> User:
        return User(
            id=self.id,
            password=password,
            access_rights=self.access_rights
        )
