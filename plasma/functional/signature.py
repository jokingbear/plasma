import inspect

from typing import Callable, Any, NamedTuple


class Signature:
    
    def __init__(self, func:Callable):
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
        default_val = ''
        if self.default is not inspect._empty:
            default_val = f'={type(self.default).__name__}'

        return f'{self.name}:{self.annotation.__name__}{default_val}'
