import typing

from .field import Field, Composite


class BaseModel:
    pass


def construct_field(cls:type, context=None):
    if type(cls) is not type or not issubclass(cls, BaseModel):
        return Field(context)
    else:
        pass
