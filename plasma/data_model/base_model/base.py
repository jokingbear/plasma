from .field import Field, Composite
from .meta import Readable
from .repr import render_lines


class BaseModel(metaclass=Readable):
    
    def __init__(self):
        for a in self.__annotations__:
            setattr(self, a, None)
    
    def __init_subclass__(cls):
        sub_fields = construct_field(cls)
        
        for name, field in sub_fields.items():
            setattr(cls, name, field)

    @classmethod
    def from_fields(cls, fields:dict[Field|Composite, object]):
        data = {}
        for field in fields:
            resolve(fields, field, data)
        
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data:dict[str, object]):
        obj = cls()
        for field_name, field_value in data.items():
            annotation = cls.__annotations__[field_name]
            if type(annotation) is Readable and issubclass(annotation, BaseModel):
                setattr(obj, field_name, annotation.from_dict(field_value))
            else:
                setattr(obj, field_name, field_value)
            
        return obj

    def __repr__(self):
        lines = []
        render_lines(None, self, lines, '')
        
        return '\n'.join(lines)


def construct_field(cls:type, context=None):
    if type(cls) is not Readable or not issubclass(cls, BaseModel): # generic type
        return Field(context)
    else:
        context = context or (cls,)
        sub_fields = {name: construct_field(annotation, (*context, name)) for name, annotation in cls.__annotations__.items()}
        if context == (cls,):
            return sub_fields
        else:
            return Composite(context, sub_fields)


def resolve(fields_values:dict[Field|Composite, object], field:Field|Composite, results:dict):
    if isinstance(field, Composite):
        for sub_field in field.sub_fields:
            resolve(fields_values, sub_field, results)
    else:
        _, *accessors, name = field.context
        
        temp_dict = results
        for a in accessors:
            if a not in temp_dict:
                temp_dict[a] = {}
            temp_dict = temp_dict[a]

        temp_dict[name] = fields_values.get(field, None)
