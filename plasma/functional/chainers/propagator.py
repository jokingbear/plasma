from typing import Callable
from .pipe import pipe


class none_propagator[I, O]:
    
    def __init__(self, func:Callable[[I], O]):
        if not isinstance(func, pipe):
            func = pipe(func)
            
        self.pipe:pipe[I, O] = func
    
    def __call__(self, inputs:I|None) -> O|None:
        if inputs is None:
            return
        
        return self.pipe(inputs)
        
    def chain[O1](self, func:Callable[[O], O1]):
        return none_propagator(self.pipe.chain(func))
    
    def automap[O1](self, func:Callable[..., O1]):
        return none_propagator(self.pipe.automap(func))

    def partial_left[O1](self, func:Callable[..., O1], *args, **kwargs):
        return none_propagator(self.pipe.partial_left(func, *args, **kwargs))

    def partial_right[O1](self, func:Callable[..., O1], *args, **kwargs):
        return none_propagator(self.pipe.partial_right(func, *args, **kwargs))
