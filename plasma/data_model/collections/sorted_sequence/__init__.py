from typing import Iterable, Callable, final

from .base import MetrizableIndex
from .defaults import identity, abs_diff

_sorted = sorted


@final
class sorted[D, K](MetrizableIndex[D, K]):
    
    def __init__(self, 
                 data:Iterable[D], 
                 key:Callable[[D], K]=identity, 
                 metric:Callable[[K, K], float]=abs_diff):
        sorted_data = _sorted(data, key=key)
        super().__init__(sorted_data, key, metric)
    
    @staticmethod
    def from_sorted[D, K](sorted_data:list[D], 
                          key:Callable[[D], K]=identity, 
                          metric:Callable[[K, K], float]=abs_diff):
        for before, after in zip(sorted_data[:-1], sorted_data[1:]):
            bkey = key(before)
            akey = key(after)
            assert bkey <= akey, f'{sorted_data} is not sorted by given key'

        return MetrizableIndex[D, K](sorted_data, key, metric)
