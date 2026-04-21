from itertools import tee
from typing import Iterable


class BaseStream[T]:
    
    def __init__(self, data:Iterable[T]):
        self._data = data
    
    @property
    def empty(self):
        for _ in self:
            return False

        return True
    
    def _clone(self):
        iter1, iter2 = tee(self._data)
        self._data = iter1
        return iter2

    def __iter__(self):
        for d in self._clone():
            yield d
