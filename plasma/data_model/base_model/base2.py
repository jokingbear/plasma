from .field import Field, Composite
from .repr import render_lines

from dataclasses import dataclass


def model(cls):
    new_cls = dataclass(cls, frozen=True)
    new_cls.__data_model = True
    
    sub_fields = construct_field(cls)
    for name, field in sub_fields.items():
        setattr(cls, name, field)

    def __repr__(self):
        lines = []
        render_lines(None, self, lines, '')
        
        return '\n'.join(lines)

    new_cls.__repr__ = __repr__
    return new_cls


def construct_field(cls:type, context=None):
    if hasattr(cls, '__data_model'):
        context = context or (cls,)
        sub_fields = {name: construct_field(annotation, (*context, name)) for name, annotation in cls.__annotations__.items()}
        if context == (cls,):
            return sub_fields
        else:
            return Composite(context, sub_fields)
    else:
        return Field(context)
