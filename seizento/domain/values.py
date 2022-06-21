from dataclasses import dataclass
from typing import Dict

from seizento.domain.identifier import Identifier


@dataclass(frozen=True)
class EncryptedString:
    metadata: str
    value: str
