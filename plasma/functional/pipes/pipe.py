import inspect

from typing import Callable, Any, NamedTuple
from abc import abstractmethod
from .readable import ReadableClass


class AutoPipe(ReadableClass):

    @abstractmethod
    def run(self, *inputs, **kwargs):...
    
    def __call__(self, *args, **kwds):
        return self.run(*args, **kwds)

    def __repr__(self):
        class_repr = super().__repr__()
        func_signature = Signature(self)
        type_name = type(self).__name__
        final_repr = f'{type_name}[{func_signature}]' + class_repr[len(type_name):]
        return final_repr


class Signature:
    
    def __init__(self, func:Callable):
        func = func.run if isinstance(func, AutoPipe) else func
        self.name = get_name(func)
        self.native = inspect.signature(func)
    
    @property
    def inputs(self):
        params = []
        for p in self.native.parameters.values():
            name = p.name
            match p.kind:
                case inspect._ParameterKind.VAR_POSITIONAL: name = '*' + name
                case inspect._ParameterKind.VAR_KEYWORD: name = '**' + name
            
            signature = Inputs(name, standardize(p.annotation), p.default)
            params.append(signature)
        return params
    
    @property
    def outputs(self):
        return standardize(self.native.return_annotation)

    def __repr__(self):
        inputs = self.inputs
        input_reps = ', '.join(str(i) for i in inputs)
        output_rep = self.outputs.__name__
        return f'({input_reps})->{output_rep}'


def get_name(func):
    if hasattr(func, '__qualname__'):
        name = func.__qualname__
    else:
        name = type(func).__name__
    
    return name


def standardize(t:type):
    if t is inspect._empty:
        return Any
    else:
        return t


class Inputs(NamedTuple):
    name:str
    annotation:type
    default:object
    
    def __repr__(self):
        annotation = ''
        if self.annotation is not Any:
            annotation = f':{self.annotation.__name__}'
        
        default_val = ''
        if self.default is not inspect._empty:
            default_val = f'={type(self.default).__name__}'

        return f'{self.name}{annotation}{default_val}'
