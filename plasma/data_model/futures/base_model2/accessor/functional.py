from collections.abc import Sequence
from typing import get_origin, get_args, Union

from .base import Accessor
from ..arch import is_model, ITEM_PREFIX, SCHEMA_FIELD


def build(name:str, t:type):
    origin = get_origin(t)
    args = get_args(t)
    
    if origin is Union and any(is_model(a) for a in args):
        raise TypeError(
            f'only support none model in Union at {name}'
        )
    
    elif origin is dict:
        raise TypeError(
            f'model does not support dict attribute at {name}'
        )
            
    children = []
    if (
        origin is not None and issubclass(origin, Sequence) #type:ignore
        and len(args) > 0 and is_model(args[0])
    ):
        children = [build(f'{ITEM_PREFIX}idx', args[0])]
    elif hasattr(t, SCHEMA_FIELD):
        children = [build(aname, atype) for aname, atype in t.__annotations__.items()]
    
    return Accessor(name, t, None, children)


def from_str(str_rep:str, value):
    accessors = str_rep.split('.')
    pass
