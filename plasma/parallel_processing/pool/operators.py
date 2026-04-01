from typing import Callable, Iterable
from .utils import Invalid, End, StreamAccumulator
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


class Unwinder[I, O](Operator[I, O], StreamAccumulator):
    
    def __init__(self, func:Callable[[I], Iterable[O]]):
        StreamAccumulator.__init__(self)
        self.func = func

    @propagate(Invalid)
    def aggregate(self, data):
        self._results.extend(self.func(data))


class Groupby[I, K, V](Operator[I, tuple[K, tuple[V]]], StreamAccumulator):
    
    def __init__(self, key:Callable[[I], K], value:Callable[[I], V]):
        StreamAccumulator.__init__(self)
        self.key = key
        self.value = value
        self._results = dict[K, list[V]](list)
    
    @propagate(Invalid)
    def aggregate(self, data):
        key = self.key(data)
        value = self.value(data)
        self._results.setdefault(key, []).append(value)

    def finalize(self):
        return self._results.items()


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
    def aggregate(self, data):
        transformed = self.selector(data)
        new_state = self.combiner(self._state, transformed)
        
        if not self.stateful:
            self._state = new_state

    def finalize(self):
        return self._state
