import numpy as np

from typing import Callable, NamedTuple, Sequence
from ..pseudo_tuple import PseudoTuple
from ...abc import Comparable
from ....functional import partials, chain, pipe


class Nearest[D, K](NamedTuple):
    arg:int
    value:D
    key:K
    dist:float


class MetrizableIndex[D, K:Comparable](PseudoTuple[D]):
    
    def __init__(
            self, 
            sorted_data:Sequence[D], 
            key:Callable[[D], K],
            metric:Callable[[K, K], float],
        ):
        super().__init__(sorted_data)
        
        self.key = key
        self.metric = metric
    
    def nearest(self, *, data:D=None, key:K|None=None) -> Nearest[D, K]:
        assert (data is not None) != (key is not None), \
                'either data or key must not be None'
        
        if key is not None:
            data_key = key
        else:
            data_key = self.key(data)

        start = 0
        end = len(self) - 1
        while end - start >= 2:
            arg = (start + end) // 2
            anchor = self[arg]
            anchor_key = self.key(anchor)
            
            if data_key == anchor_key:
                start = end = arg
            if data_key < anchor_key:
                end = arg
            elif data_key > anchor_key:
                start = arg
        
        dist = pipe(self.key) >> partials(self.metric, data_key)
        arg = min([start, end], key=lambda a: dist(self[a]))
        value = self[arg]
        return Nearest(arg, value, self.key(value), dist(value)) 

    def _slice_init(self, sliced_data):
        return MetrizableIndex(
            sliced_data,
            self.key,
            self.metric
        )
