from typing import Any, Callable, Iterable

from .base import BaseStream


class GenericStream[T](BaseStream[T]):
    
    def select[V](self, selector:Callable[[T], V]):
        for d in self:
            yield selector(d)
    
    def filter(self, *filters:Callable[[T], bool]):
        for d in self:
            if not all(f(d) for f in filters):
                continue

            yield d
    
    def unwind[V](self, roller:Callable[[T], Iterable[V]]):
        for d in self:
            yield from roller(d)
    
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
