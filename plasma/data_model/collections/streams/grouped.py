import itertools

from typing import Iterable, Sequence, Callable
from .base import BaseStream


class BasedGrouped[K, V](BaseStream[tuple[K, Sequence[V]]]):
    
    def collect[O](
            self, 
            collector:Callable[[K, Sequence[V]], O]
        ):
        for k, v in self:
            yield k, collector(k, v)

    def map[K2](self, mapper:Callable[[K], K2]):
        for k, v in self:
            yield mapper(k), v 

    def apply[V2](self, applier:Callable[[K, Sequence[V]], Sequence[V2]]):
        for k, vs in self:
            yield k, applier(k, vs)
    
    def select[T](self, selector:Callable[[K, Sequence[V]], T]):
        for k, vs in self:
            yield k, selector(k, vs)

    def filter(self, *filters:Callable[[K, Sequence[V]], bool]):
        for d in self:
            if not all(f(*d) for f in filters):
                continue
            
            yield d
                 
    def unwind[T](self, roller:Callable[[K, Sequence[V]], Iterable[T]]):
        return itertools.chain.from_iterable(roller(*d) for d in self)
    
    def accumulate[S, D](
            self, 
            initial_state:S, 
            selector:Callable[[K, Sequence[V]], D], 
            accumulator:Callable[[S, D], S|None],
            stateful=True
        ):
        new_state = initial_state
        for d in self:
            selected = selector(*d)
            temp_state = accumulator(new_state, selected)
            if not stateful and temp_state is not None:
                new_state = temp_state
        
        return new_state

    def evaluate(self):
        return dict(self)
