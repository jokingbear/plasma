from typing import Callable
from ..pipes import AutoPipe
from ..signature import Signature


class auto_map[O]:
    
    def __init__(self, func:Callable[..., O]):
        super().__init__()
        assert not isinstance(func, auto_map)
        self.func = func

    def __call__(self, inputs:tuple|list|dict[str, object]):
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
