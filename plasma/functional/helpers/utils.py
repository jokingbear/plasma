from typing import Callable
from ..pipes import Signature, AutoPipe


class proxy_func:

    def __init__(self, func):
        self.func = func

        if hasattr(func, '__qualname__'):
            self.__qualname__ = func.__qualname__

    @property
    def name(self):
        if hasattr(self.func, '__qualname__'):
            name = self.func.__qualname__
        else:
            name = type(self.func)
        
        return name
    
    @property
    def signature(self):
        return Signature(self.func)


class auto_map(AutoPipe):
    
    def __init__(self, func):
        super().__init__()
        assert not isinstance(func, auto_map)
        self.func = func

    def run(self, inputs):
        if isinstance(inputs, (tuple, list)):
            return self.func(*inputs)
        elif isinstance(inputs, dict):
            return self.func(**inputs)
        elif inputs is None:
            return self.func()
        else:
            return self.func(inputs)
    
    def type_repr(self):
        signature = Signature(self.func)
        return f'{signature.name}[automap{signature.inputs}] -> {signature.outputs.__name__}'
    
    def __repr__(self):
        return self.type_repr()


class partials(proxy_func):

    def __init__(self, func, *args, pre_apply_before=True, **kwargs):
        super().__init__(func)
        self.args = args
        self.kwargs = kwargs
        self.pre_apply_before = pre_apply_before

    def __call__(self, *new_args, **new_kwargs):
        if self.pre_apply_before:
            return self.func(*self.args, *new_args, **self.kwargs, **new_kwargs)
        else:
            return self.func(*new_args, *self.args, **new_kwargs, **self.kwargs)


class chain:

    def __init__(self, *funcs:Callable):
        assert len(funcs) > 1, 'need at least 1 func'
        self.funcs = funcs
    
    def __call__(self, *args, **kwargs):
        results = self.funcs[0](*args, **kwargs)
        for f in self.funcs[1:]:
            results = f(results)
        return results
    
    def chain(self, *funcs:Callable):
        return chain(*self.funcs, *funcs)

    def __repr__(self):
        lines = []
        offset = ''
        for f in self.funcs:
            signature = Signature(f)
            inputs_rep = ', '.join(str(i) for i in signature.inputs)
            lines.append(f'{offset}|->{signature.name}({inputs_rep}) -> {signature.outputs.__name__}')
            offset += ' ' * 3

        return '\n'.join(lines)[3:]
