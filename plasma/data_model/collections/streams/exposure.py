from itertools import chain
from typing import Any, Callable, Iterable, Sequence

from .generic import GenericStream
from .grouped import BasedGrouped
from .standard import StandardStream
from .zipped import BaseZipped
from ....functional import auto_map


class Stream[T](StandardStream[T], GenericStream[T]):
    
    def select[V](self, selector: Callable[[T], V]):
        return Stream(super().select(selector))

    def filter(self, *filters:Callable[[T], bool]):
        return Stream(super().filter(*filters))
                 
    def unwind[V](self, roller:Callable[[T], Iterable[V]]):
        return Stream(super().unwind(roller))
    
    def sort(self, key:Callable[[T], Any], reverse=False):
        return Stream(super().sort(key, reverse))
    
    def take(self, n:int):
        return Stream(super().take(n))
    
    def groupby[K, V](self, key:Callable[[T], K], value:Callable[[T], V]):
        return GroupStream(super().groupby(key, value))

    def split[*V](self, splitter:Callable[[T], tuple[*V]]):
        return ZippedStream(splitter(d) for d in self)
    
    def enumerate(self):
        return ZippedStream(enumerate(self))
    
    @staticmethod
    def from_iterable[K](iterable:Iterable[Iterable[K]]):
        return Stream(chain().from_iterable(iterable))
    
    @staticmethod
    def chain[K](*data:Iterable[K]):
        return Stream(chain(*data))


class GroupStream[K, V](BasedGrouped[K, V], GenericStream[tuple[K, Sequence[V]]]):

    def collect[O](self, collector:Callable[[K, Sequence[V]], O]):
        return Stream(super().collect(collector))

    def map_key[K2](self, mapper:Callable[[K], K2]):
        return GroupStream(super().map_key(mapper))

    def select[T](self, selector:Callable[[K, Sequence[V]], T]):
        return ZippedStream(super().select(selector))
    
    def map_value[T](self, applier:Callable[[K, Sequence[V]], Iterable[T]]):
        return GroupStream(super().map_value(applier))

    def project[T](self, projector:Callable[[K, Sequence[V]], T]):
        return Stream(projector(k, v) for k, v in self)
    
    def filter(self, *filters:Callable[[K, Sequence[V]], bool]):
        return GroupStream(super().filter(*filters))
         
    def unwind[T](self, roller:Callable[[K, Sequence[V]], Iterable[T]]):
        return Stream(super().unwind(roller))

    def sort(self, key: Callable[[K, Sequence[V]], Any], reverse=False):
        return GroupStream(super().sort(lambda kv: key(*kv), reverse))

    def take(self, n: int):
        return GroupStream(super().take(n))

    def groupby(self, key: Callable[[K, Sequence[V]], K], value: Callable[[K, Sequence[V]], V]):
        return GroupStream(super().groupby(auto_map(key), auto_map(value)))

    def max(self, key: Callable[[K, Sequence[V]], Any]):
        return super().max(key=lambda kv:key(*kv))
    
    def min(self, key: Callable[[K, Sequence[V]], Any]):
        return super().min(key=lambda kv: key(*kv))


class ZippedStream[*T](BaseZipped[*T], GenericStream[tuple[*T]]):
    
    def select[*V](self, selector:Callable[[*T], tuple[*V]]):
        return ZippedStream(super().select(selector))

    def project[V](self, projector:Callable[[*T], V]):
        return Stream(projector(*d) for d in self)

    def filter(self, *filters:Callable[[*T], bool]):
        return ZippedStream(super().filter(*filters))
                 
    def unwind[V](self, roller:Callable[[*T], Iterable[V]]):
        return Stream(super().unwind(roller))
    
    def sort(self, key:Callable[[*T], Any], reverse=False):
        return ZippedStream(super().sort(lambda d: key(*d), reverse))

    def take(self, n:int):
        return ZippedStream(super().take(n))
    
    def groupby[K, V](self, key:Callable[[*T], K], value:Callable[[*T], V]):
        return GroupStream(super().groupby(auto_map(key), auto_map(value)))

    def max(self, key:Callable[[*T], Any]):
        return super().max(key=lambda t:key(*t))
    
    def min(self, key: Callable[[*T], Any]):
        return super().min(key=lambda t:key(*t))
