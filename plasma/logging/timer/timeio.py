import time

from types import MappingProxyType
from datetime import datetime


class TimeIO:
    
    def __init__(self, name:str):
        self.name = name
        self._start = time.time()
        self._end:float = None
        self._args = None
        self._kwargs = {}

    @property
    def running(self):
        return self._end is not None
    
    @property    
    def timer(self):
        end = self._end or time.time()
        return Counter(self._start, end)
    
    def update_params(self, args:list, kwargs:dict):
        self._args = args
        self._kwargs = kwargs
    
    @property
    def args(self):
        return tuple(self._args)
    
    @property
    def kwargs(self):
        return MappingProxyType[str, object](self._kwargs)
    
    def __repr__(self):
        args = ', '.join(type(a).__name__ for a in self._args)
        kwargs = ', '.join(k for k in self._kwargs)
        return f'{type(self).__name__}({self.name}, {self.timer}, args={args}, kwargs={kwargs})'

    def finalize(self):
        assert self._end is None, 'the TimeIO has been finalized'
        self._end = time.time()
        

class Counter:
    
    def __init__(self, start:float, end:float):
        self.start = datetime.fromtimestamp(start)
        self.end = datetime.fromtimestamp(end)
    
    @property
    def duration(self):
        return self.end - self.start

    def __repr__(self):
        return f'[start={self.start}, end={self.end}, duration={self.duration}]'
