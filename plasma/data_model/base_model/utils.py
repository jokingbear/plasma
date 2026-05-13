from typing import get_origin, Iterable

from .constants import MODEL_FLAG
from .field import Field    


def is_data_model(cls:type):
    return hasattr(cls, MODEL_FLAG)


def is_list(cls:type):
    origin = get_origin(cls)
    return origin is not None and issubclass(origin, (tuple, list)) \
            or origin is None and issubclass(cls, (tuple, list)) 


def get_fields(cls:type) -> Iterable[Field]:
    assert is_data_model(cls), 'class must be a model'
    
    for n in cls.__annotations__:
        yield getattr(cls, n)
