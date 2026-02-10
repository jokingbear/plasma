from typing import Iterable, Callable
from collections import defaultdict


class groupby[K, O](dict[K, tuple[O]]):
    
    def __init__[D](self, data:Iterable[D], 
                 key:Callable[[D], K],
                 selector:Callable[[D], O]=None):
        
        selector = selector or (lambda d:d)
        temp = defaultdict(lambda: [])
        for d in data:
            dkey = key(d)
            temp[dkey].append(selector(d))
        
        for k, v in temp.items():
            self[k] = tuple(v)
