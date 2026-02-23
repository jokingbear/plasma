from typing import dataclass_transform
from dataclasses import dataclass

from .field import Field, Composite
from .repr import render_lines


FIELD_FLAG = '__fields' 
MODEL_FLAG = '__data_model'

@dataclass_transform()
def model(cls):
    new_cls = register_field(cls)
    setattr(cls, MODEL_FLAG, True)
    new_cls.__data_model = True
    
    def __repr__(self):
        lines = []
        render_lines(None, self, lines, '')
        
        return '\n'.join(lines)

    new_cls.__repr__ = __repr__
    return dataclass(new_cls, repr=False)


def register_field[T](cls:type[T]) -> type[T]:
    setattr(cls, FIELD_FLAG, True)
    sub_fields = _construct_field(cls)
    for name, field in sub_fields.items():
        setattr(cls, name, field)
    
    return cls


def _construct_field(cls:type, context=None):
    if hasattr(cls, FIELD_FLAG):
        context = context or (cls,)
        sub_fields = {name: _construct_field(annotation, (*context, name)) for name, annotation in cls.__annotations__.items()}
        if context == (cls,):
            return sub_fields
        else:
            return Composite(context, sub_fields)
    else:
        return Field(context)
