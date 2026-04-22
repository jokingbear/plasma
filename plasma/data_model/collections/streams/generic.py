from typing import Any, Callable

from .base import BaseStream


class GenericStream[T](BaseStream[T]):
    
    def sort(self, key:Callable[[T], Any], reverse=False):
        return sorted(self, key=key, reverse=reverse)

    def take(self, n:int):
        for i, d in enumerate(self):
            if i >= n:
                break
            
            yield d
