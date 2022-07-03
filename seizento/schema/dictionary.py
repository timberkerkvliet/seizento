from dataclasses import dataclass
from typing import Dict

from seizento.path import PathComponent, MatchComponent
from seizento.schema.schema import Schema


@dataclass(frozen=True)
class Dictionary(Schema):
    value_type: Schema

    @property
    def default_value(self) -> Dict:
        return {}

    def is_subschema(self, other: Schema) -> bool:
        if not isinstance(other, Dictionary):
            return False

        return self.value_type.is_subschema(other.value_type)

    def supports_child_at(self, component: PathComponent) -> bool:
        return isinstance(component, MatchComponent)
