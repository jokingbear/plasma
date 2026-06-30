from typing import Any, Callable
from .pipe import pipe


class partial_left[O]:
    
    def __init__(self, func:Callable[..., O], *args, **kwargs):
        if not isinstance(func, pipe):
            func = pipe(func)

        self.args = args
        self.kwargs = kwargs
        self.pipe = func
    
    def __call__(self, *args: Any, **kwds: Any) -> O:
        func_stack = [*self.pipe.func_stack()][::-1]
        
        results = func_stack[1](*self.args, *args, **self.kwargs, **kwds)
        for f in func_stack[2:]:
            results = f(results)
        return results
        
    def chain[O1](self, func:Callable[[O], O1]):
        return partial_left(self.pipe.chain(func), *self.args, **self.kwargs)
    
    def automap[O1](self, func:Callable[..., O1]):
        return partial_left(self.pipe.automap(func), *self.args, **self.kwargs)


class partial_right[O]:
    
    def __init__(self, func:Callable[..., O], *args, **kwargs):
        if not isinstance(func, pipe):
            func = pipe(func)

        self.args = args
        self.kwargs = kwargs
        self.pipe = func
    
    def __call__(self, *args: Any, **kwds: Any) -> O:
        func_stack = [*self.pipe.func_stack()][::-1]
        
        results = func_stack[1](*args, *self.args, **kwds, **self.kwargs)
        for f in func_stack[2:]:
            results = f(results)
        return results
        
    def chain[O1](self, func:Callable[[O], O1]):
        return partial_right(self.pipe.chain(func), *self.args, **self.kwargs)
    
    def automap[O1](self, func:Callable[..., O1]):
        return partial_right(self.pipe.automap(func), *self.args, **self.kwargs)
