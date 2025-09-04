"""Utility Enum di base con helper comuni."""

from enum import Enum


class BaseEnum(Enum):
    """Enum base che restituisce il valore come stringa e fornisce utility."""

    def __str__(self):
        return str(self.value)

    @classmethod
    def all(cls):
        """Restituisce la lista dei valori dell'enum."""
        return list(map(lambda c: c.value, cls))

    @staticmethod
    def extend_enum(base_enum, name, extra_members: dict):
        """Crea dinamicamente un nuovo Enum estendendo `base_enum` con membri extra."""
        members = {**base_enum.__members__, **extra_members}
        return BaseEnum(name, members, type=base_enum.__bases__[0], module=__name__)
