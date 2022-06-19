from dataclasses import dataclass
from typing import Dict

from seizento.domain.identifier import Identifier


@dataclass(frozen=True)
class EncryptedStringLiteral:
    metadata: str
    value: str

    def to_json(self) -> Dict:
        return {
            'metadata_': self.metadata,
            'value': self.value
        }

    @classmethod
    def from_json(cls, value: Dict):
        if set(value.keys()) != {'public_key_id', 'encrypted_value'}:
            raise ValueError
        return cls(
            public_key_id=Identifier(value['public_key_id']),
            encrypted_value=
        )
