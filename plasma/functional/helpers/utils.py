from typing import Callable
from ..pipes import AutoPipe, SequentialPipe
from ..signature import Signature


class auto_map(AutoPipe):
    
    def __init__(self, func):
        super().__init__()
        assert not isinstance(func, auto_map)
        self.func = func

    def run(self, inputs):
        if isinstance(inputs, (tuple, list)):
            return self.func(*inputs)
        elif isinstance(inputs, dict):
            return self.func(**inputs)
        elif inputs is None:
            return self.func()
        else:
            return self.func(inputs)
    
    def __repr__(self):
        return repr(self.signature())

    def signature(self):
        if isinstance(self.func, AutoPipe):
            signature = self.func.signature()
        else:
            signature = Signature.from_func(self.func)

        return Signature(
            signature.name,
            f'automap({signature.inputs})',
            signature.outputs
        )


class chain(SequentialPipe):

    def __init__(self, *funcs:Callable):
        assert len(funcs) > 1, 'need at least 1 func'
        super().__init__(**{f'pipe_{i}': f for i, f in enumerate(funcs)})
    
    def run(self, *args, **kwargs):
        results = self.funcs[0](*args, **kwargs)
        for f in self.funcs[1:]:
            results = f(results)
        return results
    
    def chain(self, *funcs:Callable):
        return chain(*self.funcs, *funcs)
