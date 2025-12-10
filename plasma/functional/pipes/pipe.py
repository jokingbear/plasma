from .readable import ReadableClass
from ..signature import Signature


class AutoPipe(ReadableClass):

    def run(self, *inputs, **kwargs):...
    
    def __call__(self, *args, **kwds):
        return self.run(*args, **kwds)
    
    def signature(self):
        signature = Signature.from_func(self.run)
        signature = Signature(type(self).__name__, signature.inputs, signature.outputs)
        return signature
