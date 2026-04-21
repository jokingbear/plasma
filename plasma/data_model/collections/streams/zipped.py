import itertools

from typing import Callable, Iterable

from .base import BaseStream


class BaseZipped[*T](BaseStream[tuple[*T]]):
    
    def select[*V](self, selector:Callable[[*T], tuple[*V]]):
        for d in self:
            yield selector(*d)

    def filter(self, *filters:Callable[[*T], bool]):
        for d in self:
            if not all(f(*d) for f in filters):
                continue
            
            yield d
                 
    def unwind[V](self, roller:Callable[[*T], Iterable[V]]):
        return itertools.chain.from_iterable(roller(*d) for d in self)
    
    def accumulate[S, D](
            self, 
            initial_state:S, 
            selector:Callable[[*T], D], 
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
        return list(self)
