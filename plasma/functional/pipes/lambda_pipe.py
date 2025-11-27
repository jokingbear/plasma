from .pipe import AutoPipe
from warnings import deprecated, warn


@deprecated('this class is deprecated')
class LambdaPipe(AutoPipe):
    
    def __init__(self, func):
        super().__init__()
        warn('this class is deprecated, just use func directly')
        self.func = func
    
    def run(self, *inputs, **kwargs):
        return self.func(*inputs, **kwargs)

    def __repr__(self):
        return f'Lambda({repr(self.func)})'
