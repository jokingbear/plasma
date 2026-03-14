import numpy as np

from typing import Callable, NamedTuple
from ..pseudo_tuple import PseudoTuple
from ....functional import partials, chain


class Nearest[D, K](NamedTuple):
    arg:int
    value:D
    key:K
    dist:float


class MetrizableIndex[D, K](PseudoTuple[D]):
    
    def __init__(self, 
                sorted_data:list[D], 
                key:Callable[[D], K],
                metric:Callable[[K, K], float],
            ):
        super().__init__(sorted_data)
        
        self.key = key
        self.metric = metric or _abs_diff
    
    def nearest(self, *, data:D=None, key:K=None) -> Nearest[D, K]:
        assert (data is not None) ^ (key is not None), \
                'either data or key must not be None'
        
        if data is not None:
            data_key = self.key(data)
        else:
            data_key = key
        
        sorted_array = self._data
        arg = len(sorted_array) // 2
        candidate_key = self.key(sorted_array[arg])
        offset = 0
        dist = chain(
                    self.key,
                    partials(self.metric, data_key),
                )
        while len(sorted_array) > 0:
            if len(sorted_array) <= 2:
                arg = min(
                        range(len(sorted_array)), 
                        key=lambda a: (dist(sorted_array[a]), -a)
                    )
                candidate = self[offset + arg]
                candidate_key = self.key(candidate)
                return Nearest(offset + arg, candidate, candidate_key, dist(candidate))
            elif data_key <= candidate_key:
                sorted_array = sorted_array[:arg + 1]
            elif data_key > candidate_key:
                sorted_array = sorted_array[arg:]
                offset += arg
            
            arg = len(sorted_array) // 2
            candidate_key = self.key(sorted_array[arg])
    
    def _slice_init(self, sliced_data):
        return MetrizableIndex(
            sliced_data,
            self.key,
            self.metric
        )
