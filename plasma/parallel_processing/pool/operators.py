from collections import defaultdict
from typing import Callable, Iterable
from .utils import Invalid, End, StreamAccumulator
from ..communicators.distributors import Distributor
from ...functional.decorators import propagate


class Operator[I, O]:...


class Init[I](Operator[I, I]):...


class Simple[I, O](Operator[I, O]):
    
    def __init__(self, func:Callable[[I], O]):
        super().__init__()
        self.func = func
    
    @propagate(End)
    @propagate(Invalid)
    def __call__(self, inputs:I):
        return self.func(inputs)


class Unwinder[I, O](Operator[I, O], Distributor):
    
    def __init__(self, func:Callable[[I], Iterable[O]]):
        Distributor.__init__(self)
        self.func = func

    def run(self, data, *queues, **named_queues):
        if data is End or data is Invalid:
            for q in queues:
                q.put(data)
        else:
            for q in queues:
                for d in self.func(data):
                    q.put(d)


class Groupby[I, K, V](Operator[I, tuple[K, tuple[V]]], StreamAccumulator):
    
    def __init__(self, key:Callable[[I], K], value:Callable[[I], V]):
        StreamAccumulator.__init__(self)
        self.key = key
        self.value = value
        self._results = defaultdict[K, list[V]](list)
    
    @propagate(End)
    @propagate(Invalid)
    def aggregate(self, data):
        key = self.key(data)
        value = self.value(data)
        self._results[key].append(value)

    def finalize(self):
        return dict(self._results)


class Accumulator[I, D, S](Operator[I, S], StreamAccumulator):
    
    def __init__(
            self, initial_state:S,
            selector:Callable[[I], D],
            combiner:Callable[[S, D], S|None],
            stateful=True
        ):
        StreamAccumulator.__init__(self)
        
        self._state = initial_state
        
        self.selector = selector
        self.combiner = combiner
        self.stateful = stateful
    
    @propagate(Invalid)
    @propagate(End)
    def aggregate(self, data):
        transformed = self.selector(data)
        new_state = self.combiner(self._state, transformed)
        
        if not self.stateful:
            self._state = new_state

    def finalize(self):
        return self._state
