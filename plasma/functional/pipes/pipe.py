import inspect

from abc import abstractmethod
from .readable import ReadableClass


class AutoPipe(ReadableClass):

    @abstractmethod
    def run(self, *inputs, **kwargs):...
    
    def __call__(self, *args, **kwds):
        return self.run(*args, **kwds)

    def __repr__(self):
        class_repr = super().__repr__()
        
        signature = inspect.signature(self.run)
        params = render_params(signature)
        params = ', '.join(params)
        return_signature = render_annotation(signature.return_annotation)
        
        return f'{class_repr}:F[[{params}], {return_signature}]'


def render_params(signature:inspect.Signature):
    params = []
    for p in signature.parameters.values():
        if p.name != 'self':
            params.append(f'{p.name}:{render_annotation(p.annotation)}')
    
    return params


def render_annotation(t:type|inspect._empty):
    if t is inspect._empty:
        return 'Any'
    else:
        return t.__name__
