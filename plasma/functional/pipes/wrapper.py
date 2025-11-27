from .pipe import AutoPipe, Signature
from typing import Callable, Any


class Wrapper[T](AutoPipe):
    
    def __init__(self, func:Callable[[T], Any]):
        super().__init__()
        
        self.func = func
    
    def run(self, inputs:tuple, **kwargs):
        *meta, data = inputs
        return *meta, self.func(data, **kwargs)

    def __repr__(self):
        type_name = type(self).__name__
        
        if isinstance(self.func, AutoPipe):
            method_name = type(self.func).__name__
            signature = Signature(self.func.run)
        else:
            method_name = self.func.__qualname__
            signature = Signature(self.func)
        
        input_rep = ', '.join(str(i) for i in signature.inputs)
        return f'{type_name}(*meta, {method_name}({input_rep}))->tuple[*meta, {signature.outputs.__name__}]'

    def type_repr(self):
        return repr(self)
