from typing import dataclass_transform, get_args
from dataclasses import dataclass

from .constants import MODEL_FLAG, FIELD_FLAG, ACCESSORS
from .field import Field, Composite, List
from .repr import render_lines
from .inquirer import is_list, is_data_model


@dataclass_transform()
def model(cls):
    new_cls = register_field(cls)
    setattr(cls, MODEL_FLAG, True)
    
    def __repr__(self):
        lines = []
        render_lines(None, self, lines, '')
        
        return '\n'.join(lines)

    new_cls.__repr__ = __repr__
    setattr(new_cls, ACCESSORS, Accessors(cls))
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


class Accessors(dict[str, type]):
    
    def __init__(self, model_cls:type):
        super().__init__()
        
        for a in model_cls.__annotations__:
            self.__update(getattr(model_cls, a))
    
    def __update(self, field:Field):
        if isinstance(field, Composite):
            for f in field.sub_fields.values():
                self.__update(f)
        elif isinstance(field, List):
            if is_data_model(field.cls):
                accessors = Accessors(field.cls)
                current_accessor = field.accessor + '.@idx.'
                for a, t in accessors.items():
                    self[current_accessor + a] = t
            else:
                self[field.accessor] = list, tuple
        else:
            self[field.accessor] = field.cls or object
