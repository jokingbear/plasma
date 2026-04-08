from typing import Callable


class pipe[I, O]:
    
    def __init__(self, func:Callable[[I], O]):
        self.func = func

    def __call__(self, inputs:I):
        return self.func(inputs)
    
    def __rshift__[I, O](self, other:Callable[[I], O]):
        return chain[I, O](self, other)
    
    def __repr__(self):
        return repr(self.func)


class chain[I, O]:...
class chain[I, O]:
    
    def __init__[T](self, prev:chain[I, T]|pipe[I, T], func:Callable[[T], O]):
        self.prev = prev
        self.func = func
    
    def __call__(self, inputs:I) -> O:
        funcs = []
        current = self
        while True:
            funcs.insert(0, current.func)
            if isinstance(current, pipe):
                break
            current = current.prev
        
        results = inputs
        for f in funcs:
            results = f(results)
        
        return results
    
    def __rshift__[T](self, other:Callable[[O], T]):
        return chain[I, T](self, other)
    
    def __repr__(self):
        return (
                f'{repr(self.prev)}\n'
                f'--> {repr(self.func)}'
            )
