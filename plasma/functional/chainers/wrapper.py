from typing import Callable
from .pipe import pipe


class wrap[I, O]:
    
    def __init__(self, func:Callable[[I], O]):
        if not isinstance(func, pipe):
            func = pipe(func)
        
        self.pipe = func
    
    def __call__[*T](self, inputs:tuple[*T, I]) -> tuple[*T, O]:
        funcs = [*self.pipe.func_stack()][::-1]
        *meta, input = inputs
        
        results = funcs[1](input)
        for f in funcs[2:]:
            results = f(results)
        
        return *meta, results #type:ignore
    
    def chain[T](self, other:Callable[[O], T]):
        return wrap[I, T](self.pipe.chain(other))

    def partial_left[O1](self, func:Callable[..., O1], *args, **kwargs):
        return wrap[I, O1](self.pipe.partial_left(func, *args, **kwargs))

    def partial_right[O1](self, func:Callable[..., O1], *args, **kwargs):
        return wrap[I, O1](self.pipe.partial_right(func, *args, **kwargs))

    def automap[O2](self, func:Callable[..., O2]):
        return wrap[I, O2](self.pipe.automap(func))
