from dataclasses import dataclass
from typing import Dict

from seizento.expression.expression import Expression
from seizento.identifier import Identifier
from seizento.schema.schema import Schema
from seizento.user import User


@dataclass
class ApplicationData:
    schema: Schema
    expression: Expression
    users: Dict[Identifier, User]
