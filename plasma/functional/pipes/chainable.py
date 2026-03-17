from typing import Callable


class Chain[**I, O]:
    
    def __call__(self, *args:I.args, **kwds:I.kwargs) -> O:...
    
    def chain[O2](self, other:Callable[[O], O2]):
        return Chained(self, other)

    @staticmethod
    def cast[**I, O](func:Callable[I, O]):
        return InitChain(func)


class Chained[**I, O2](Chain[I, O2]):
    
    def __init__[O](self, 
                    func1:Callable[I, O],
                    func2:Callable[[O], O2]
                ):
        super().__init__()
        
        self.func1 = func1
        self.func2 = func2
    
    def __call__(self, *args, **kwds):
        results = self.func1(*args, **kwds)
        return self.func2(results)

    def __repr__(self):
        rep1 = repr(self.func1)
        rep2 = repr(self.func2)
        return f'{rep1}\n--> {rep2}'


class InitChain[**I, O](Chain[I, O]):
    
    def __init__(self, func:Callable[I, O]):
        super().__init__()
        self.func = func
    
    def __call__(self, *args, **kwds):
        return self.func(*args, **kwds)

    def __repr__(self):
        return repr(self.func)
