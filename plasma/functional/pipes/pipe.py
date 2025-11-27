import inspect

from abc import abstractmethod
from .readable import ReadableClass
from typing import NamedTuple
from ..signature import Signature


class AutoPipe(ReadableClass):

    @abstractmethod
    def run(self, *inputs, **kwargs):...
    
    def __call__(self, *args, **kwds):
        return self.run(*args, **kwds)

    def __repr__(self):
        class_repr = super().__repr__()
        func_signature = Signature(self.run)
        type_name = type(self).__name__
        final_repr = f'{type_name}[{func_signature}]' + class_repr[len(type_name):]
        return final_repr
