from typing import dataclass_transform, get_args
from dataclasses import dataclass

from .constants import MODEL_FLAG, FIELD_FLAG
from .field import Field, Composite, List
from .repr import Repr
from .inquirer import is_list
from .schemas import Schema


@dataclass_transform()
def model(cls):
    new_cls = register_field(cls)
    setattr(cls, MODEL_FLAG, True)
    setattr(cls, MODEL_FLAG, Schema(new_cls))

    def __repr__(self):
        return Repr()(self)
    
    new_cls.__repr__ = __repr__
    return dataclass(new_cls, repr=False)


def register_field[T](cls:type[T]) -> type[T]:
    setattr(cls, FIELD_FLAG, True)
    composite:Composite = _construct_field(cls)
    for name, field in composite.sub_fields.items():
        setattr(cls, name, field)
    
    return cls


def _construct_field(cls:type, context=None):
    if hasattr(cls, FIELD_FLAG):
        context = context or (cls,)
        sub_fields = {name: _construct_field(annotation, (*context, name)) for name, annotation in cls.__annotations__.items()}
        return Composite(context, cls, sub_fields)
    elif is_list(cls):
        args = get_args(cls)
        contained_cls = None
        if len(args) > 0:
            contained_cls = args[0]
        return List(context, contained_cls)
    else:
        return Field(context, cls)
