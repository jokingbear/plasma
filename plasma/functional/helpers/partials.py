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


def partial_left[O](func:Callable[..., O], *args, **kwargs):
    def alt_func(*new_args, **new_kwargs):
        return func(*args, *new_args, **kwargs, **new_kwargs)

    return alt_func


def partial_right[O](func:Callable[..., O], *args, **kwargs):
    def alt_func(*new_args, **new_kwargs):
        return func(*new_args, *args, **new_kwargs, **kwargs)

    return alt_func
