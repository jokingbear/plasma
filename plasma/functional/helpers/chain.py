from typing import Callable
from ..pipes import AutoPipe
from ..signature import Signature


class chain(AutoPipe):

    def __init__(self, *funcs:Callable):
        assert len(funcs) > 1, 'need at least 1 func'
        super().__init__()
        self.funcs = funcs
    
    def run(self, *args, **kwargs):
        results = self.funcs[0](*args, **kwargs)
        for f in self.funcs[1:]:
            results = f(results)
        return results
    
    def chain(self, *funcs:Callable):
        return chain(*self.funcs, *funcs)
    
    def signature(self):
        first_func = self.funcs[0]
        if isinstance(first_func, AutoPipe):
            first_signature = first_func.signature()
        else:
            first_signature = Signature.from_func(first_func)
        
        last_func = self.funcs[-1]
        if isinstance(last_func, AutoPipe):
            last_signature = last_func.signature()
        else:
            last_signature = Signature.from_func(last_func)

        return Signature(
            'chain',
            first_signature.inputs,
            last_signature.outputs
        )
