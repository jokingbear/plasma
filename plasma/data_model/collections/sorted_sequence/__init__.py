from typing import Iterable, Callable

from .base import MetrizableIndex
from .defaults import identity, abs_diff

_sorted = sorted


def sorted[D, K](
        data:Iterable[D], 
        key:Callable[[D], K]=identity,
        metric:Callable[[K, K], float]=abs_diff
    ):
    sorted_list = _sorted(data, key=key)
    return MetrizableIndex[D, K](sorted_list, key, metric)
