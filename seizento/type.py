from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Optional, List, Callable, Any

from seizento.identifier import Identifier, NodeIdentifier


@dataclass(frozen=True)
class Type(ABC):
    secret: bool

    @property
    @abstractmethod
    def default_value(self):
        pass

    @property
    @abstractmethod
    def is_functional(self) -> bool:
        pass

    @abstractmethod
    def get_node(self, identifier: NodeIdentifier) -> Type:
        pass


@dataclass(frozen=True)
class Struct(Type):
    fields: Dict[Identifier, Type]

    def __post_init__(self):
        non_secret_field_names = {
            field.name for field, field_type in self.fields.items()
            if not field_type.secret
        }
        if self.secret and non_secret_field_names:
            raise ValueError(
                f'The following field(s) are non-secret:'
                f'{non_secret_field_names}'
            )

    @property
    def default_value(self) -> Optional[Dict]:
        return {
            field.name: field_type.default_value
            for field, field_type in self.fields.items()
        }

    @property
    def is_functional(self) -> bool:
        return any(field_type.is_functional for field_type in self.fields.values())

    def get_node(self, identifier: NodeIdentifier) -> Type:
        if identifier.root not in self.fields:
            raise KeyError

        return self.fields[identifier.root].get_node(identifier.path_as_identifier)


@dataclass(frozen=True)
class Array(Type):
    value_type: Type

    def __post_init__(self):
        if self.secret and not self.value_type.secret:
            raise ValueError(f'The value type is non-secret')

    @property
    def default_value(self) -> Optional[List]:
        return []

    @property
    def is_functional(self) -> bool:
        return self.value_type.is_functional

    def get_node(self, identifier: NodeIdentifier) -> Type:
        return self.value_type.get_node(identifier)


@dataclass(frozen=True)
class Dictionary(Type):
    value_type: Type

    def __post_init__(self):
        if self.secret and not self.value_type.secret:
            raise ValueError(f'The value type is non-secret')

    @property
    def default_value(self) -> Optional[Dict]:
        return {}

    @property
    def is_functional(self) -> bool:
        return self.value_type.is_functional

    def get_node(self, identifier: NodeIdentifier) -> Type:
        return self.value_type.get_node(identifier)


@dataclass(frozen=True)
class Function(Type):
    value_type: Type

    def __post_init__(self):
        if self.secret and not self.value_type.secret:
            raise ValueError(f'The value type is non-secret')

    @staticmethod
    def _default_function(arg: str):
        raise KeyError

    @property
    def default_value(self) -> Optional[Callable[[str], Any]]:
        return self._default_function

    @property
    def is_functional(self) -> bool:
        return True

    def get_node(self, identifier: NodeIdentifier) -> Type:
        return self.value_type.get_node(identifier)


@dataclass(frozen=True)
class Primitive(Type, ABC):
    optional: bool

    @property
    @abstractmethod
    def default_literal(self):
        pass

    @property
    def default_value(self):
        if self.default_literal is not None:
            return self.default_literal
        if self.optional:
            return None

        raise ValueError('No default value available')

    @property
    def is_functional(self) -> bool:
        return False

    def get_node(self, identifier: NodeIdentifier) -> Type:
        raise KeyError


@dataclass(frozen=True)
class String(Primitive):
    default_literal: Optional[str] = None


@dataclass(frozen=True)
class Integer(Primitive):
    default_literal: Optional[int] = None


@dataclass(frozen=True)
class Float(Primitive):
    default_literal: Optional[float] = None


@dataclass(frozen=True)
class Boolean(Primitive):
    default_literal: Optional[bool] = None
