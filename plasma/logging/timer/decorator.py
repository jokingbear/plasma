from collections.abc import Callable
from functools import wraps
from .timeio import TimeIO


class Timer:

    IO = TimeIO

    def __init__(self, 
            log_func:Callable[[TimeIO], None]|None=None, 
            name:str|None=None
        ):
        self.log_func = log_func
        self.name = name or ''
        self._io:TimeIO|None = None
    
    def init(self):
        timeio = TimeIO(self.name)
        self._io = timeio
        return timeio
    
    def __enter__(self):
        return self.init()

    def __exit__(self, *_):
        if self._io is None:
            return

        self._io.finalize()
        log_func = self.log_func or print
        log_func(self._io)
        self._io = None

    def __call__[**I, O](self, func:Callable[I, O]):
        name = func.__qualname__
        self.name = name
        
        @wraps(func)
        def timed_func(*args:I.args, **kwargs:I.kwargs) -> O:
            with self as timeio:
                results = func(*args, **kwargs)
                timeio.update_params(args, kwargs)

            return results
        
        return timed_func
