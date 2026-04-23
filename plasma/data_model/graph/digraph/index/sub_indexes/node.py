from typing import Any, Callable, Iterable


class NodeSubIndex:
    
    def __init__(self, key:Callable[[Any], Any]):
        self._dict = dict[Any, set]()
        self.key = key
        self._len = 0
    
    def get_nodes(self, keys:Any|Iterable) -> Iterable:
        if not isinstance(keys, Iterable):
            keys = [keys]

        for k in keys:
            yield from self._dict.get(k, [])
    
    def add(self, node_id:Any):
        key = self.key(node_id)
        if key is None:
            return

        node_set = self._dict.setdefault(key, set())
        if node_id not in node_set:
            node_set.add(node_id)
            self._len += 1
    
    def delete(self, node_id):
        key = self.key(node_id)
        if key not in self._dict:
            return

        node_set = self._dict[key]
        if node_id not in node_set:
            return

        node_set.remove(node_id)
        if len(node_set) == 0:
            del self._dict[key]

    def __contains__(self, node_id):
        key = self.key(node_id)
        return (
            key in self._dict
            and node_id in self._dict[key]
        )

    def __len__(self):
        return self._len
