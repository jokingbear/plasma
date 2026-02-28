import numpy as np

from typing import Iterable, Callable

from ..tuple_interface import PseudoTuple
from ....functional import partials, chain


class MetrizableDataKeyIndex[D, K](PseudoTuple[D]):
    
    def __init__(self, 
                sorted_data:list[D], 
                key:Callable[[D], K],
                metric:Callable[[K, K], float]=None
            ):
        super().__init__(sorted_data)
        
        self.key = key
        self.metric = metric
    
    def nearest(self, *, data:D=None, key:K=None) -> tuple[int, float]:
        assert data is not None ^ key is not None
        
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
                    partials(self._metric, data_key)
                )
        while len(sorted_array) > 0:
            if len(sorted_array) <= 2:
                arg = min(
                        range(len(sorted_array)), 
                        key=lambda a: dist(sorted_array[a])
                    )
                candidate = self[offset + arg]
                candidate_key = self.key(candidate)
                return offset + arg, dist(candidate_key)
            elif data_key < candidate_key:
                sorted_array = sorted_array[:arg + 1]
            elif input > sorted_array[arg]:
                sorted_array = sorted_array[arg:]
                offset += arg
            
            arg = len(sorted_array) // 2
            candidate_key = self.key(self._sorted_data[arg])
    
    def _slice_init(self, sliced_data):
        return MetrizableDataKeyIndex(
            sliced_data,
            self.key,
            self.metric
        )
