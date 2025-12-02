from ..pipes import AutoPipe
from ..signature import Signature


class partials(AutoPipe):

    def __init__(self, func, *args, pre_apply_before=True, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.pre_apply_before = pre_apply_before

    def run(self, *new_args, **new_kwargs):
        if self.pre_apply_before:
            return self.func(*self.args, *new_args, **self.kwargs, **new_kwargs)
        else:
            return self.func(*new_args, *self.args, **new_kwargs, **self.kwargs)
    
    def __repr__(self):
        return repr(self.signature())
    
    def signature(self):
        if isinstance(self.func, AutoPipe):
            signature = self.func.signature()
        else:
            signature = Signature.from_func(self.func)
        
        args = []        
        for a in self.args:
            args.append(type(a).__name__)
        args = ','.join(args)
        
        kwargs = []
        for k, v in self.kwargs.items():
            kwargs.append(f'{k}={type(v).__name__}')
        kwargs = ','.join(kwargs)
        
        name = f'{signature.name}[{','.join([args, kwargs])}]'
        return Signature(
            name,
            signature.inputs,
            signature.outputs
        )
