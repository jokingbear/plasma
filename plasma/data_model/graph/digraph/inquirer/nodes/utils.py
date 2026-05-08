import inspect

from typing import Callable, Hashable
from .tuple_dict import TupleDict
from .....base_model import Field


def compile[T](
        inquirer_type:type[T], 
        selector:str|Field|Callable[..., object]
    ) -> str|Field|Callable[[Hashable, T, TupleDict], object]:
    if not callable(selector):
        return selector
    
    signature = inspect.signature(selector)
    has_args = any(p.kind is inspect._ParameterKind.VAR_POSITIONAL 
                for p in signature.parameters.values())
    parameters = {k:p for k, p in signature.parameters.items() if k != 'self'}
    
    if has_args or len(parameters) >= 3:
        return selector
    elif len(parameters) == 2:
        def alt_func(node:Hashable, inquirer:T, td:TupleDict):
            return selector(node, inquirer)
        
        return alt_func
    else:
        def alt_func(node:Hashable, inquirer:T, td:TupleDict):
            return selector(node)

        return alt_func


def select_node(node, _):
    return node
