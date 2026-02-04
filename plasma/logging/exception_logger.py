from functools import wraps
from dataclasses import dataclass
from typing import Callable, Any


@dataclass
class ExceptionIO:
    name:str
    args:list
    kwargs:dict
    exception:Exception


class ExceptionLogger[V]:

    IO = ExceptionIO
    
    def __init__(self, name=None, 
                 log_func:Callable[[ExceptionIO], None]=print, raise_on_exception=True, 
                 on_exception_return:Callable[[ExceptionIO], V]|V=None) -> None:
        self.name = name
        self.log_func = log_func
        self.raise_on_exception = raise_on_exception
        self.on_exception_value = on_exception_return
    
    def __call__[**I, O](self, function:Callable[I, O]):
        name = self.name or function.__qualname__
        
        @wraps(function)
        def run(*args:I.args, **kwargs:I.kwargs) -> O|V:
            try:
                results = function(*args, **kwargs)
                return results
            except Exception as e:
                exio = ExceptionIO(name, args, kwargs, e)
                self.log_func(exio)
                
                if self.raise_on_exception:
                    raise e
                
                if callable(self.on_exception_value):
                    return self.on_exception_value(exio)
                return self.on_exception_value

        return run
