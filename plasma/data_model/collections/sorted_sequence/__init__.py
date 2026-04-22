from typing import Iterable, Callable, final, Sequence

from .base import MetrizableIndex
from .defaults import identity, abs_diff
from ...abc import Comparable

_sorted = sorted


@final
class sorted[D, K:Comparable](MetrizableIndex[D, K]):
    
    def __init__(self, 
                 data:Iterable[D], 
                 key:Callable[[D], K]=identity, 
                 metric:Callable[[K, K], float]=abs_diff):
        sorted_data = _sorted(data, key=key)
        super().__init__(sorted_data, key, metric)
    
    @staticmethod
    def from_sorted[U, V:Comparable](
            sorted_data:Sequence[U], 
            key:Callable[[U], V]=identity, 
            metric:Callable[[V, V], float]=abs_diff
        ):
        for before, after in zip(sorted_data[:-1], sorted_data[1:]):
            bkey = key(before)
            akey = key(after)
            assert bkey <= akey, f'{sorted_data} is not sorted by given key'

        return MetrizableIndex[U, V](sorted_data, key, metric)
