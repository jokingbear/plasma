from typing import Callable, Iterable


class Operator[I, O]:...


class Simple[I, O](Operator[I, O]):
    
    def __init__(self, func:Callable[[I], O]):
        super().__init__()
        self.func = func


class Unwinder[I, O](Operator[I, O]):
    
    def __init__(self, func:Callable[[I], Iterable[O]]):
        super().__init__()
        self.func = func


class Groupby[I, K, V](Operator[I, tuple[K, tuple[V]]]):
    
    def __init__(self, key:Callable[[I], K], value:Callable[[I], V]):
        super().__init__()
        self.key = key
        self.value = value
