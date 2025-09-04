from enum import Enum


class BaseEnum(Enum):
    def __str__(self):
        return str(self.value)

    @classmethod
    def all(cls):
        return list(map(lambda c: c.value, cls))

    # funzione di utilità per “estendere” un Enum
    @staticmethod
    def extend_enum(base_enum, name, extra_members: dict):
        # __members__ è un OrderedDict dei membri di base_enum
        members = {**base_enum.__members__, **extra_members}
        return BaseEnum(name, members, type=base_enum.__bases__[0], module=__name__)
