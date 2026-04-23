from typing import Callable


class partials[O]:

    def __init__(self, func:Callable[..., O], *args, pre_apply_before=True, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.pre_apply_before = pre_apply_before

    def __call__(self, *new_args, **new_kwargs):
        if self.pre_apply_before:
            return self.func(*self.args, *new_args, **self.kwargs, **new_kwargs)
        else:
            return self.func(*new_args, *self.args, **new_kwargs, **self.kwargs)
