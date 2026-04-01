import itertools
from itertools import tee
from typing import Iterable, Callable

from .chain import Chain
from .flow import Flow
from .operators import Simple, Unwinder, Groupby, Accumulator, Init
from .utils import Invalid
from ...data_model.collections import groupby, Stream as SimpleStream


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
        if isinstance(self.chain, Init):
            return Stream[V](
                self.id, 
                itertools.chain.from_iterable(unwinder(d) for d in self.data), 
                Chain(None, Init()), self.resolver
            )

        new_chain = self.chain.next(Unwinder(unwinder))
        counter = 0
        with self.resolver(new_chain) as flow:
            for d in self._clone():
                flow.put(d)
                counter += 1
            
            data = flow.accumulator.wait(total=counter, desc='unwinding')

        return Stream[V](self.id, data, Init[V](), self.resolver)
    
    def groupby[K, V](self, key:Callable[[T], K], value:Callable[[T], V]):
        if isinstance(self.chain, Init):
            return Stream[tuple[K, tuple[V]]](
                self.id, 
                groupby(self.data, key, value).items(), 
                Chain(None, Init()), self.resolver
            )

        new_chain = self.chain.next(Groupby(key, value))
        counter = 0
        with self.resolver(new_chain) as flow:
            for d in self._clone():
                flow.put(d)
                counter += 1
            
            grouped = flow.accumulator.wait(total=counter, desc='grouping')

        return Stream[tuple[K, tuple[V]]](self.id, grouped, Init(), self.resolver)
    
    def accumulate[S, D](
            self, initial_state:S, 
            selector:Callable[[T], D], 
            accumulator:Callable[[S, D], S|None],
            stateful=True
        ) -> S:
        if isinstance(self.chain, Init):
            return SimpleStream(self.data).accumulate(initial_state, selector, accumulator, stateful)

        new_chain = self.chain.next(Accumulator(initial_state, selector, accumulator, stateful))
        counter = 0
        with self.resolver(new_chain) as flow:
            for d in self._clone():
                flow.put(d)
                counter += 1
            
            return flow.accumulator.wait(counter)
    
    def to_list(self) -> list[T]:
        if isinstance(self.chain, Init):
            return list(self._clone())

        counter = 0
        with self.resolver(self.chain) as flow:
            for d in self._clone():
                flow.put(d)
                counter += 1

            return flow.accumulator.wait(counter)
    
    def _clone(self):
        iter1, iter2 = tee(self.data)
        self.data = iter1
        return iter2

    def __iter__(self):
        for d in self.to_list():
            yield d
