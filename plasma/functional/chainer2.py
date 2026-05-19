from typing import Any, Callable
from .identity import identity


class pipe[I, O]:
    
    def __init__[T](self, func:Callable[[T], O], prev:Callable[[I], T]=identity):
        self.prev = prev
        self.func = func

    def __call__(self, inputs:I) -> O:
        funcs = []
        current = self.prev
        while True:
            if isinstance(current, pipe):
                funcs.append(current.func)
                current = current.prev
            else:
                funcs.append(current)
                break

        funcs = funcs[::-1]
        results = inputs
        for f in funcs:
            results = f(results)
        
        return self.func(results) #type: ignore - lib limit
    
    def chain[T](self, other:Callable[[O], T]):
        return pipe(other, self)

    def partial_left[O1](self, func:Callable[..., O1], *args, **kwargs):
        def alt_func(a:O):
            return func(*args, a, **kwargs)
        
        return pipe(alt_func, self)

    def partial_right[O1](self, func:Callable[..., O1], *args, **kwargs):
        def alt_func(a:O):
            return func(a, *args, **kwargs)
        
        return pipe(alt_func, self)

    def __rshift__[T](self, other:Callable[[O], T]):
        return self.chain(other)


class auto_map[O](pipe[tuple|list|dict[str, object], O]):
    
    def __init__(self, func:Callable[..., O]):
        super().__init__(func)

    def __call__(self, inputs:tuple|list|dict[str, object]):
        if isinstance(inputs, (tuple, list)):
            return self.func(*inputs)
        elif isinstance(inputs, dict):
            return self.func(**inputs) #type:ignore
        elif inputs is None:
            return self.func()
        else:
            return self.func(inputs)


class partial_left[O](pipe[Any, O]):
    
    def __init__(self, func:Callable[..., O], *args, **kwargs):
        super().__init__(func)
        self.args = args
        self.kwargs = kwargs
    
    def __call__(self, inputs):
        return self.func(*self.args, inputs, **self.kwargs) #type: ignore lib limit
    

class partial_right[O](pipe[Any, O]):
    
    def __init__(self, func:Callable[..., O], *args, **kwargs):
        super().__init__(func)
        self.args = args
        self.kwargs = kwargs
    
    def __call__(self, inputs):
        return self.func(inputs, *self.args, **self.kwargs) #type: ignore lib limit
