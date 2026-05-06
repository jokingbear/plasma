from typing import Callable, Any


class pipe[I, O]:
    
    def __init__(self, func:Callable[[I], O]):
        self.func = func

    def __call__(self, inputs:I):
        return self.func(inputs)
    
    def __rshift__[V](self, other:Callable[[O], V]):
        return chain[I, V](self, other)
    
    def chain[V](self, other:Callable[[O], V]):
        return chain[I, V](self, other)
    
    def __repr__(self):
        return repr(self.func)


class chain[I, O]:
    
    def __init__(self, prev:Callable[[I], Any], func:Callable[[Any], O]):
        self.prev = prev
        self.func = func
    
    def __call__(self, inputs:I) -> O:
        funcs = []
        current = self.prev
        while True:
            if isinstance(current, chain):
                funcs.append(current.func)
                current = current.prev
            else:
                funcs.append(current)
                break

        funcs = funcs[::-1]
        results = inputs
        for f in funcs:
            results = f(results)
        
        return self.func(results)
    
    def __rshift__[T](self, other:Callable[[O], T]):
        return chain[I, T](self, other)
    
    def chain[T](self, other:Callable[[O], T]):
        return chain[I, T](self, other)
    
    def __repr__(self):
        return (
                f'{repr(self.prev)}\n'
                f'--> {repr(self.func)}'
            )
