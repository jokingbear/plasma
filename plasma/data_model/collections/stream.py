from itertools import tee, chain
from typing import Callable, Iterable

from .group import groupby


class Stream[T]:
    
    def __init__(self, data:Iterable[T]):
        self._data = data
    
    def select[V](self, selector:Callable[[T], V]):
        return Stream(selector(d) for d in self)

    def filter(self, *filters:Callable[[T], bool]):
        return Stream(d for d in self if all(f(d) for f in filters))
    
    def accumulate[S, D](self, initial_state:S, 
                         selector:Callable[[T], D],
                         accumulator:Callable[[D], S], stateful=True):
        state = initial_state
        for d in self:
            temp_data = selector(d)
            new_state = accumulator(temp_data)
            if not stateful:
                state = new_state
        
        return state
    
    def unwind[V](self, func:Callable[[T], Iterable[V]]):
        return Stream(v for d in self 
                      for v in func(d))
    
    def groupby[K, V](self, key:Callable[[T], K], value:Callable[[T], V]=None, as_stream=True):
        group = groupby(self, key, value)
        
        if as_stream:
            return Stream(group.items())
        else:
            return group
    
    def sort[K](self, key:Callable[[T], K]=None, reverse=False):
        return Stream[T](sorted(self, key=key, reverse=reverse))
    
    def evaluate(self):
        return [*self]
    
    def empty(self):
        for _ in self:
            return False

        return True
    
    @staticmethod
    def from_iterable[T](iterable:Iterable[Iterable[T]]):
        return Stream(chain.from_iterable(iterable))
    
    @staticmethod
    def chain[T](*data:Iterable[T]):
        return Stream(chain(*data))
    
    def _clone(self):
        iter1, iter2 = tee(self._data)
        self._data = iter1
        return iter2

    def __iter__(self):
        for d in self._clone():
            yield d
