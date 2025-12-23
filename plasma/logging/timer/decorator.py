from .timeio import TimeIO
from typing import Callable
from functools import wraps


class Timer:

    IO = TimeIO

    def __init__(self, log_func:Callable[[TimeIO], None]=None, name=None) -> None:
        self.log_func = log_func
        self.name = name or ''
        self._io:TimeIO = None

    def __enter__(self):
        timeio = TimeIO(self.name)
        self._io = timeio
        return timeio

    def __exit__(self, *_):
        self._io.finalize()
        log_func = self.log_func or print
        log_func(self._io)
        self._io = None

    def __call__(self, func):
        name = func.__qualname__
        self.name = name
        
        @wraps(func)
        def timed_func(*args, **kwargs):
            with self as timeio:
                results = func(*args, **kwargs)
                timeio.update_params(args, kwargs)

            return results
        
        return timed_func
