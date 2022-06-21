from typing import TypeVar

from seizento.domain.types.type import Type

T = TypeVar('T')


class Primitive(Type):
    @property
    def default_value(self):
        return None

    @property
    def is_functional(self) -> bool:
        return False

    def get_subtypes(self):
        return None


class String(Primitive):
    pass


class EncryptedString(Primitive):
    pass


class Boolean(Primitive):
    pass


class Float(Primitive):
    pass


class Integer(Primitive):
    pass

