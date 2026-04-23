from networkx import DiGraph
from typing import Any, Callable, Iterable


class NodeSubIndex:
    
    def __init__(self, key:Callable[[Any], Any]):
        self._internal_dict = dict[Any, set]()
        self._key = key
    
    def get_nodes(self, value) -> Iterable:
        return self._internal_dict.get(value, [])
    
    def get_value(self, node_id):
        return self._key(node_id)
    
    def add(self, node_id:Any):
        key = self._key(node_id)
        if key is None:
            return

        self._internal_dict.setdefault(key, set()).add(node_id)
    
    def delete(self, node_id):
        value = self.get_value(node_id)
        if value is not None:
            return

        node_set = self._internal_dict.setdefault(value, {node_id})
        node_set.remove(node_id)
        if len(node_set) == 0:
            del self._internal_dict[value]

    def __contains__(self, node_id):
        return node_id in self._internal_dict
