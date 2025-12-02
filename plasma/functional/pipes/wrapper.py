from .pipe import AutoPipe
from typing import Callable, Any
from ..signature import Signature


class Wrapper(AutoPipe):
    
    def __init__(self, func:Callable):
        super().__init__()
        
        self.func = func
    
    def run(self, inputs:tuple, **kwargs):
        *meta, data = inputs
        return *meta, self.func(data, **kwargs)

    def __repr__(self):        
        signature = self.signature()
        return f'{signature.name}({signature.inputs})->{signature.outputs}'
    
    def signature(self):
        if isinstance(self.func, AutoPipe):
            original_signature = self.func.signature()
        else:
            original_signature = Signature.from_func(self.func)

        return Signature(
            type(self).__name__,
            f'*meta, {original_signature.name}({original_signature.inputs})',
            f'tuple[*meta, {original_signature.outputs}]'
        )
