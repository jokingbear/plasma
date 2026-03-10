from typing import get_origin, Iterator

from .constants import MODEL_FLAG
from .field import Field

    
def is_data_model(cls:type):
    return hasattr(cls, MODEL_FLAG)
    

def fields(cls:type) -> Iterator[Field]:
    assert is_data_model(cls)
    
    for a in cls.__annotations__:
        yield getattr(cls, a)


def is_list(cls:type):
    origin = get_origin(cls)
    return origin is not None and issubclass(origin, (tuple, list)) \
            or origin is None and issubclass(cls, (tuple, list)) 
