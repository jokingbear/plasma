from collections import defaultdict
from typing import Callable, Iterable
from warnings import deprecated

from .color_printer import Color


def _identity(x):
    return x


@deprecated('use plasma.data_model.collections.groupby instead')
class groupby[K, V](dict[K, tuple[V]]):
        
    def __init__[D](self, 
                    data:Iterable[D], 
                    key:Callable[[D], K],
                    selector:Callable[[D], V]=_identity,
                ):
        temp = defaultdict(list)
        for d in data:
            dkey = key(d)
            temp[dkey].append(selector(d))
        
        for k, v in temp.items():
            self[k] = tuple(v)
        
        print(Color.YELLOW.render('use plasma.data_model.collections.groupby instead'))
