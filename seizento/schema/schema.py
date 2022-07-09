from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional

from seizento.path import PathComponent


class Schema(ABC):
    @abstractmethod
    def is_subschema(self, other: Schema) -> bool:
        pass

    @abstractmethod
    def can_add_child(self, component: PathComponent) -> bool:
        pass

    @abstractmethod
    def can_remove_child(self, component: PathComponent) -> bool:
        pass

    @abstractmethod
    def common_superschema(self, other: Schema) -> Optional[Schema]:
        pass
