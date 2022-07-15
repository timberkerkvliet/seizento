from dataclasses import dataclass
from typing import Dict

from seizento.expression.expression import Expression
from seizento.identifier import Identifier
from seizento.path import PathComponent, Path, LiteralComponent
from seizento.schema.schema import Schema
from seizento.user import User


@dataclass
class Root:
    schema: Schema
    expression: Expression
