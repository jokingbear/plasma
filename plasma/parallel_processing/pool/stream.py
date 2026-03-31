from itertools import tee
from typing import Iterable, Callable

from .chain import Chain
from .flow import Flow
from .operators import Simple, Unwinder, Groupby
from .utils import Invalid


class Stream[T]:
    
    def __init__[I](
            self, data:Iterable[I], chain:Chain[I, T], 
            resolver:Callable[[Chain[I, T]], Flow[T]]
        ):
        self.data = data
        self.chain = chain
        self.resolver = resolver
    
    def select[V](self, selector:Callable[[T], V]):
        return Stream(self._data, self.chain.next(Simple(selector)), self.resolver)
    
    def filter(self, *funcs:Callable[[T], bool]):
        def alt_filter(inputs:T) -> T:
            if all(f(inputs) for f in funcs):
                return inputs
            else:
                return Invalid

        return Stream(self._data, self.chain.next(Simple(alt_filter)), self.resolver)

    def unwind[V](self, unwinder:Callable[[T], Iterable[V]]):
        return Stream(self.data, self.chain.next(Unwinder(unwinder)), self.resolver)
    
    def groupby[K, V](self, key:Callable[[T], K], value:Callable[[T], V]):
        return Stream(self.data, self.chain.next(Groupby(key, value)), self.resolver)
    
    def _clone(self):
        iter1, iter2 = tee(self._data)
        self.data = iter1
        return iter2

    def __iter__(self):
        flow = self.resolver(self.chain)
        with flow:
            counter = 0
            for d in self._clone():
                flow.put(d)
                counter += 1
            
            data = flow.accumulator.wait(total=counter)

        for d in data:
            yield d
