import inspect

from typing import Any, NamedTuple
from types import UnionType


class Signature(NamedTuple):
    name:str
    inputs:str
    outputs:str

    def __repr__(self):
        return f'{self.name}({self.inputs}) -> {self.outputs}'

    @staticmethod
    def from_func(func):
        name = func.__qualname__ if hasattr(func, '__qualname__') else type(func).__name__
        native = inspect.signature(func)
        return_type = standardize(native.return_annotation)
        return_str = render_type(return_type)
        return Signature(name, render_inputs(native), return_str)


def render_inputs(signature:inspect.Signature):
    params = []
    for p in signature.parameters.values():
        name = p.name
        match p.kind:
            case inspect._ParameterKind.VAR_POSITIONAL: name = '*' + name
            case inspect._ParameterKind.VAR_KEYWORD: name = '**' + name

        param_str = render_single_input(name, standardize(p.annotation), p.default)
        params.append(param_str)
    return ', '.join(params)


def render_single_input(name:str, annotation:type, default):
    annotation_str = render_type(annotation, render_any=False)
    if len(annotation_str) > 0:
        annotation_str = ':' + annotation_str
    
    
    default_str = ''
    if default is not inspect._empty:
        default_str = f'={type(default).__name__}'

    return f'{name}{annotation_str}{default_str}'


def standardize(t:type):
    if t is inspect._empty:
        return Any
    else:
        return t


def render_type(t:type, render_any=True):
    if hasattr(t, '__args__'):
        args = [render_type(a) for a in t.__args__]
        if isinstance(t, UnionType):
            args = '|'.join(args)
            return args
        else:
            args = ','.join(args)
            return f'{t.__name__}[{args}]'
    elif t is Any and not render_any:
        return ''
    else:
        return t.__name__
