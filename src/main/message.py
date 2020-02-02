# import enum
from aenum import Enum

class Message(Enum):

    def describe(self):
        return self.name, self.value

    def __str__(self):
        # return 'custom str! {0}'.format(self.value)
        return self.value

    @classmethod
    def favorite_mood(cls):
        return cls.happy

    
    def enum(*sequential, **named):
        enums = dict(zip(sequential, range(len(sequential))), **named)
        return type('Enum', (), enums)

    def enum_class(classname, *values):
        cls = type(classname, (), {})
        cls._mapping = {}
        for value in values:
            attribute = value.upper().replace(' ', '_')
            instance = cls()
            setattr(cls, attribute, instance)
            instance.value = value
            cls._mapping[value] = instance
        cls.from_string = lambda value: cls._mapping.get(value)
        cls.__str__ = lambda self: self.value
        return cls


    def to_string(self):
        return self.value

    def format_string(self, *args):
        return self.value.format(*args)
