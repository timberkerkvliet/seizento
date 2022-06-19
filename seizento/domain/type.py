from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Optional, List, Callable, Any

from seizento.domain.identifier import Identifier
from seizento.domain.path import Path, PathValue, PlaceHolder


@dataclass(frozen=True)
class Type(ABC):
    @property
    @abstractmethod
    def default_value(self):
        pass

    @property
    @abstractmethod
    def is_functional(self) -> bool:
        pass

    @abstractmethod
    def get_subtype(self, path: Path) -> Type:
        pass


@dataclass(frozen=True)
class Struct(Type):
    fields: Dict[Identifier, Type]

    @property
    def default_value(self) -> Optional[Dict]:
        return {
            field.name: field_type.default_value
            for field, field_type in self.fields.items()
        }

    @property
    def is_functional(self) -> bool:
        return any(field_type.is_functional for field_type in self.fields.values())

    def get_subtype(self, path: Path) -> Type:
        if path.empty:
            return self

        component = path.first_component
        if not isinstance(component, PathValue):
            raise TypeError

        identifier = Identifier(component.value)
        if identifier not in self.fields:
            raise KeyError

        field_type = self.fields[identifier]
        return field_type.get_subtype(path.remove_first_component())


@dataclass(frozen=True)
class Array(Type):
    value_type: Type

    @property
    def default_value(self) -> Optional[List]:
        return []

    @property
    def is_functional(self) -> bool:
        return self.value_type.is_functional

    def get_subtype(self, path: Path) -> Type:
        if path.empty:
            return self

        component = path.first_component
        if not isinstance(component, PlaceHolder):
            raise TypeError

        return self.value_type.get_subtype(path.remove_first_component())


@dataclass(frozen=True)
class Dictionary(Type):
    value_type: Type

    @property
    def default_value(self) -> Optional[Dict]:
        return {}

    @property
    def is_functional(self) -> bool:
        return self.value_type.is_functional

    def get_subtype(self, path: Path) -> Type:
        if path.empty:
            return self

        component = path.first_component
        if not isinstance(component, PlaceHolder):
            raise TypeError

        return self.value_type.get_subtype(path.remove_first_component())


@dataclass(frozen=True)
class Function(Type):
    value_type: Type

    @staticmethod
    def _default_function(arg: str):
        raise KeyError

    @property
    def default_value(self) -> Optional[Callable[[str], Any]]:
        return self._default_function

    @property
    def is_functional(self) -> bool:
        return True

    def get_subtype(self, path: Path) -> Type:
        if path.empty:
            return self

        component = path.first_component
        if not isinstance(component, PlaceHolder):
            raise TypeError

        return self.value_type.get_subtype(path.remove_first_component())


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

    def get_subtype(self, path: Path) -> Type:
        if path.empty:
            return self

        raise TypeError


@dataclass(frozen=True)
class EncryptedString(Primitive):
    def default_literal(self):
        return None


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
