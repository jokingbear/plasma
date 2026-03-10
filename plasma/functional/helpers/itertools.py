from typing import Iterable, Callable
from collections import defaultdict


class groupby[K, V](dict[K, tuple[V]]):
    
    def __init__[D](self, 
                    data:Iterable[D], 
                    key:Callable[[D], K],
                    selector:Callable[[D], V]=None
                ):
        
        selector = selector or _identity
        temp = defaultdict(list)
        for d in data:
            dkey = key(d)
            temp[dkey].append(selector(d))
        
        for k, v in temp.items():
            self[k] = tuple(v)


def _identity(x):
    return x
