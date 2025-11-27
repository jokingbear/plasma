import inspect

from functools import wraps


class propagate:

    def __init__(self, value=None):
        self.value = value
    
    def __call__(self, func):
        signature = inspect.signature(func)

        is_instance_method = 'self' in signature.parameters
        propagator = self

        @wraps(func)    
        def alt_func(*args, **kwargs):
            if is_instance_method:
                inputs = args[1]
            else:
                inputs = args[0]

            if inputs is propagator.value:
                return propagator.value
            else:
                return func(*args, **kwargs)

        return alt_func
