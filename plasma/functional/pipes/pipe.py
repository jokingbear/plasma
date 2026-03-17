from typing import Callable
from functools import wraps

from .chainable import Chain
from .readable import ReadableClass
from ..signature import Signature


class AutoPipe[**I, O](ReadableClass, Chain[I, O]):

    def run(self, *inputs, **kwargs) -> O:...
    
    def __call__(self, *args:I.args, **kwds:I.kwargs) -> O:
        return self.run(*args, **kwds)
    
    def signature(self):
        signature = Signature.from_func(self.run)
        signature = Signature(type(self).__name__, signature.inputs, signature.outputs)
        return signature
