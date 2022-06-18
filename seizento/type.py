from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Optional, List, Callable, Any


@dataclass(frozen=True)
class Identifier:
    name: str

    def __post_init__(self):
        if not self.name.replace('_', '').replace('-', '').isalnum():
            raise ValueError(f'Invalid identifier: {self.name}')

    def __str__(self):
        return self.name


@dataclass(frozen=True)
class Type(ABC):
    secret: bool
    optional: bool

    @property
    @abstractmethod
    def default_value(self):
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
    def default_value(self) -> Dict:
        return {
            field.name: field_type.default_value
            for field, field_type in self.fields.items()
        }


@dataclass(frozen=True)
class Array(Type):
    value_type: Type

    def __post_init__(self):
        if self.secret and not self.value_type.secret:
            raise ValueError(f'The value type is non-secret')

    @property
    def default_value(self) -> List:
        return []


@dataclass(frozen=True)
class Dictionary(Type):
    value_type: Type

    def __post_init__(self):
        if self.secret and not self.value_type.secret:
            raise ValueError(f'The value type is non-secret')

    @property
    def default_value(self) -> Dict:
        return {}


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
    def default_value(self) -> Callable[[str], Any]:
        return self._default_function


@dataclass(frozen=True)
class String(Type):
    has_default: bool = True
    default_value: Optional[str] = None


@dataclass(frozen=True)
class Integer(Type):
    default_value: Optional[int] = None


@dataclass(frozen=True)
class Float(Type):
    default_value: Optional[float] = None


@dataclass(frozen=True)
class Boolean(Type):
    default_value: Optional[bool] = None


s = Struct(
    secret=True,
    optional=False,
    fields={
        Identifier('a_hold'): String(secret=True, optional=False),
        Identifier('another-field'): Integer(secret=True, optional=True)
    }
)

print(s.default_value)
