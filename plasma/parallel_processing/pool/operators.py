from typing import Callable, Iterable
from .utils import Invalid, End
from ..communicators.accumulators import DynamicAccumulator
from ..communicators.distributors import IteratorDistributor
from ...functional.decorators import propagate


class Operator[I, O]:...


class Init[I](Operator[I, I]):...


class Simple[I, O](Operator[I, O]):
    
    def __init__(self, func:Callable[[I], O]):
        super().__init__()
        pipe = propagate(Invalid)(func)
        pipe = propagate(End)(func)
        self.pipe = pipe


class Unwinder[I, O](Operator[I, O]):
    
    def __init__(self, func:Callable[[I], Iterable[O]]):
        super().__init__()
        self.pipe = IteratorDistributor()


class Groupby[I, K, V](Operator[I, tuple[K, tuple[V]]]):
    
    def __init__(self, key:Callable[[I], K], value:Callable[[I], V]):
        super().__init__()
        self.key = key
        self.value = value
        self.pipe = DynamicAccumulator[I, dict[K, tuple[V]]]()
