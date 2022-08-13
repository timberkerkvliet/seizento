from dataclasses import dataclass
from typing import Dict

from seizento.identifier import Identifier
from seizento.schema.schema import Schema
from seizento.user import User, ADMIN_USER
from seizento.value.value import Value


@dataclass
class ApplicationData:
    schema: Schema
    value: Value
    users: Dict[Identifier, User]


def create_default() -> ApplicationData:
    return ApplicationData(
        schema=Schema(schema={'type': 'object', 'additionalProperties': False}),
        value=Value({}),
        users={ADMIN_USER.id: ADMIN_USER}
    )
