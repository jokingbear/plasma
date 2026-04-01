from itertools import tee
from typing import Iterable, Callable

from .chain import Chain
from .flow import Flow
from .operators import Simple, Unwinder, Groupby, Accumulator
from .utils import Invalid, End


class Stream[T]:
    
    def __init__[I](
            self, id:object, data:Iterable[I], chain:Chain[I, T], 
            resolver:Callable[[Chain], Flow],
        ):
        self._id = id
        self.data = data
        self.chain = chain
        self.resolver = resolver
    
    @property
    def id(self):
        return self._id
    
    def select[V](self, selector:Callable[[T], V]):
        return Stream(self.id, self.data, self.chain.next(Simple(selector)), self.resolver)
    
    def filter(self, *funcs:Callable[[T], bool]):
        def alt_filter(inputs:T) -> T:
            if all(f(inputs) for f in funcs):
                return inputs
            else:
                return Invalid

        return Stream(self.id, self.data, self.chain.next(Simple(alt_filter)), self.resolver)

    def unwind[V](self, unwinder:Callable[[T], Iterable[V]]):
        return Stream(self.id, self.data, self.chain.next(Unwinder(unwinder)), self.resolver)
    
    def groupby[K, V](self, key:Callable[[T], K], value:Callable[[T], V]):
        return Stream(self.id, self.data, self.chain.next(Groupby(key, value)), self.resolver)
    
    def accumulate[S, D](
            self, initial_state:S, 
            selector:Callable[[T], D], 
            accumulator:Callable[[S, D], S|None],
            stateful=True
        ) -> S:
        new_chain = self.chain.next(Accumulator(initial_state, selector, accumulator, stateful))
        flow = self.resolver(new_chain)
        with flow:
            for d in self._clone():
                flow.put(d)
            
            return flow.accumulator.wait()
    
    def to_list(self) -> list[T]:
        flow = self.resolver(self.chain)
        with flow:
            counter = 0
            for d in self._clone():
                flow.put(d)
                counter += 1
            flow.put(End)
            return flow.accumulator.wait(total=counter)
    
    def _clone(self):
        iter1, iter2 = tee(self.data)
        self.data = iter1
        return iter2

    def __iter__(self):
        for d in self.to_list():
            yield d
