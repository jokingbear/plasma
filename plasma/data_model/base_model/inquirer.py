from typing import get_args, get_origin
from .constants import MODEL_FLAG
    

def is_data_model(cls:type):
    return hasattr(cls, MODEL_FLAG)
    

def fields(cls:type):
    assert is_data_model(cls), 'class must be data model'
    
    return cls.__annotations__


def is_list(cls:type):
    origin = get_origin(cls)
    return origin is not None and issubclass(origin, (tuple, list)) \
            or origin is None and issubclass(cls, (tuple, list)) 
