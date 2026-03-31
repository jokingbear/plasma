from collections import defaultdict
from typing import Callable, Iterable
from .utils import Invalid, End
from ..communicators.accumulators import DynamicAccumulator
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


class Groupby[I, K, V](Operator[I, tuple[K, tuple[V]]], DynamicAccumulator[I, dict[K, tuple[V]]]):
    
    def __init__(self, key:Callable[[I], K], value:Callable[[I], V]):
        DynamicAccumulator.__init__(self)
        self.key = key
        self.value = value
        self._end = False
        self._results = defaultdict[K, list[V]](list)
    
    def run(self, data):
        self._end = data is End
        return super().run(data)
    
    @property
    def finished(self):
        return self._end
    
    @propagate(End)
    @propagate(Invalid)
    def aggregate(self, data):
        key = self.key(data)
        value = self.value(data)
        self._results[key].append(value)

    def finalize(self):
        return dict(self._results)
