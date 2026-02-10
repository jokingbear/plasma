from typing import Iterable, Callable
from collections import defaultdict


class groupby[T, V](dict[V, tuple[T]]):
    
    def __init__(self, data:Iterable[T], 
                 key:Callable[[T], V]):
        
        temp = defaultdict(lambda: [])
        for d in data:
            dkey = key(d)
            temp[dkey].append(d)
        
        for k, v in temp.items():
            self[k] = tuple(v)
