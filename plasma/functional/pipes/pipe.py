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
            annotation = p.annotation.__name__ if p.annotation is not inspect._empty else 'Any'
            name = p.name
            match p.kind:
                case inspect._ParameterKind.VAR_POSITIONAL: name = '*' + name
                case inspect._ParameterKind.VAR_KEYWORD: name = '**' + name

            default_val = ''
            if p.default is not inspect._empty:
                default_val = f'={type(p.default).__name__}'
            params.append(f'{name}:{annotation}{default_val}')
    
    return params


def render_annotation(t:type|inspect._empty):
    if t is inspect._empty:
        return 'Any'
    else:
        return t.__name__
