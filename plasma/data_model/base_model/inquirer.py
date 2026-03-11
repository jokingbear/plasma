from typing import get_origin, Mapping

from .constants import MODEL_FLAG
from .field import Field
from .schemas import AccessorSchema, StructSchema
    
def is_data_model(cls:type):
    return hasattr(cls, MODEL_FLAG)
    

def accessors(cls:type) -> Mapping[str, Field]:
    assert is_data_model(cls)
    return AccessorSchema(cls)


def struct(cls:type) -> Mapping:
    assert is_data_model(cls)
    return StructSchema(AccessorSchema(cls))


def is_list(cls:type):
    origin = get_origin(cls)
    return origin is not None and issubclass(origin, (tuple, list)) \
            or origin is None and issubclass(cls, (tuple, list)) 
