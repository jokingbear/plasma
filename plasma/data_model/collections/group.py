from collections.abc import Iterable, Callable
from collections import defaultdict
from warnings import deprecated


def _identity[T](x:T):
    return x


@deprecated('use stream instead', stacklevel=2)
class groupby[K, V](dict[K, tuple[V]]):
    
    def __init__[D](self, 
                    data:Iterable[D], 
                    key:Callable[[D], K],
                    selector:Callable[[D], V]=None, #type:ignore
                ):
        selector = selector or _identity
        temp = defaultdict(list)
        for d in data:
            dkey = key(d)
            temp[dkey].append(selector(d))
        
        for k, v in temp.items():
            self[k] = tuple(v)
