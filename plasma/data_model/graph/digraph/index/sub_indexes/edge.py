import itertools
from typing import Any, Callable, Iterable


class EdgeSubindex:
    
    def __init__(self, type_getter:Callable[[Any], Any]) -> None:
        self.type_getter = type_getter
        self._dict = dict[Any, dict[Any, set]]()
    
    def add(self, nid, mid):
        mtype = self.type_getter(mid)

        self._dict\
        .setdefault(nid, {})\
        .setdefault(mtype, set()).add(mid)
    
    def delete(self, nid, mid):
        if nid not in self._dict:
            return
        
        mtype = self.type_getter(mid)
        data = self._dict[nid]
        if mtype not in data:
            return
        
        node_set = data[mtype]
        if mid not in node_set:
            return
        node_set.remove(mid)
        if len(node_set) == 0:
            del data[mtype]
        
        if len(data) == 0:
            del self._dict[nid]
    
    def get(self, nid, mtype=None) -> Iterable:
        data = self._dict.get(nid, dict())
        
        if mtype is None:
            return itertools.chain(data.values())
        else:
            return data.get(mtype, [])  
    
    def __contains__(self, edge):
        u, v = edge
        vtype = self.type_getter(v)
        return (
            u in self._dict 
            and vtype in self._dict[u]
            and v in self._dict[u][vtype]
        )
