from typing import TypeVar, Generic, Optional, Dict

from seizento.domain.path import PathComponent
from seizento.domain.types.type import Type

T = TypeVar('T')


class EncryptedString(Type):
    def __init__(self, optional: bool):
        self._optional = optional

    @property
    def is_optional(self) -> bool:
        return self._optional

    @property
    def default_value(self):
        raise ValueError('No default value available')

    @property
    def is_functional(self) -> bool:
        return False

    def get_subtypes(self):
        return None


class String(Type):
    def __init__(self, optional: bool, default_value: Optional[str]):
        self._optional = optional
        self._default_value = default_value

    @property
    def is_optional(self) -> bool:
        return self._optional

    @property
    def default_value(self) -> Optional[str]:
        if self._default_value:
            return self._default_value

        if self._optional:
            return None

        raise ValueError('No default value available')

    @property
    def is_functional(self) -> bool:
        return False

    def get_subtypes(self) -> Dict[PathComponent, Type]:
        return None


class Integer(Type):
    def __init__(self, optional: bool, default_value: Optional[int]):
        self._optional = optional
        self._default_value = default_value

    @property
    def is_optional(self) -> bool:
        return self._optional

    @property
    def default_value(self) -> Optional[int]:
        if self._default_value:
            return self._default_value

        if self._optional:
            return None

        raise ValueError('No default value available')

    @property
    def is_functional(self) -> bool:
        return False

    def get_subtypes(self):
        return None


class Float(Type):
    def __init__(self, optional: bool, default_value: Optional[float]):
        self._optional = optional
        self._default_value = default_value

    @property
    def is_optional(self) -> bool:
        return self._optional

    @property
    def default_value(self) -> Optional[float]:
        if self._default_value:
            return self._default_value

        if self._optional:
            return None

        raise ValueError('No default value available')

    @property
    def is_functional(self) -> bool:
        return False

    def get_subtypes(self):
        return None


class Boolean(Type):
    def __init__(self, default_value: Optional[str]):
        self._default_value = default_value

    @property
    def default_value(self) -> T:
        if self._default_value is None:
            raise ValueError('No default value available')

        return self._default_value

    @property
    def is_functional(self) -> bool:
        return False

    def get_subtypes(self):
        return None
