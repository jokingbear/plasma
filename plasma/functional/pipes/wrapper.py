from .pipe import AutoPipe
from typing import Callable


class Wrapper[T](AutoPipe):
    
    def __init__(self, func:Callable[[T]]):
        super().__init__()
        
        self.func = func
    
    def run(self, inputs:tuple, **kwargs):
        *meta, data = inputs
        return *meta, self.func(data, **kwargs)
