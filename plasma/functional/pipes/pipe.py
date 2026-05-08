from warnings import deprecated
from .chainable import Chain
from .readable import ReadableClass
from ..signature import Signature


@deprecated(
    'AutoPipe is deprecated, use __call__ combine with ReadableClass '
    'for better python signature support'
)
class AutoPipe[**I, O](ReadableClass, Chain[I, O]):
    
    def __init__(self):
        super().__init__()

    def run(self, *inputs, **kwargs) -> O:...
    
    def __call__(self, *args:I.args, **kwds:I.kwargs) -> O:
        return self.run(*args, **kwds)
    
    def signature(self):
        signature = Signature.from_func(self.run)
        signature = Signature(type(self).__name__, signature.inputs, signature.outputs)
        return signature
