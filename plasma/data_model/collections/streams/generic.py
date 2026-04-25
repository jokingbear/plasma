from typing import Any, Callable, Sequence

from .base import BaseStream


class GenericStream[T](BaseStream[T]):
    
    def sort(self, key:Callable[[T], Any], reverse=False):
        return sorted(self, key=key, reverse=reverse)

    def take(self, n:int):
        for i, d in enumerate(self):
            if i >= n:
                break
            
            yield d

    def groupby[K, V](self, key:Callable[[T], K], value:Callable[[T], V]):
        data = dict[K, list[V]]()
        for d in self:
            data.setdefault(key(d), []).append(value(d))

        yield from data.items()

    def max(self, key:Callable[[T], Any]):
        return max(self, key=key)
    
    def min(self, key:Callable[[T], Any]):
        return min(self, key=key)
