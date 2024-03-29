from dataclasses import dataclass
from typing import Dict

from seizento.identifier import Identifier
from seizento.schema import Schema
from seizento.user import User, ADMIN_USER
from seizento.value import Value


@dataclass
class AppData:
    schema: Schema
    value: Value
    users: Dict[Identifier, User]


def create_default() -> AppData:
    return AppData(
        schema=Schema(schema={'type': 'object', 'additionalProperties': False}),
        value=Value({}),
        users={ADMIN_USER.id: ADMIN_USER}
    )
