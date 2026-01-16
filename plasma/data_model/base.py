from .field import Field, Composite


class BaseModel:
    
    def __init_subclass__(cls):
        sub_fields = construct_field(cls)
        
        for name, field in sub_fields.items():
            setattr(cls, name, field)


def construct_field(cls:type, context=None):
    if type(cls) is not type or not issubclass(cls, BaseModel): # generic type
        return Field(context)
    else:
        context = context or (cls.__name__,)
        sub_fields = {name: construct_field(annotation, (*context, name)) for name, annotation in cls.__annotations__.items()}
        if context == (cls.__name__,):
            return sub_fields
        else:
            return Composite(context, sub_fields)
