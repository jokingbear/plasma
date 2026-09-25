from collections.abc import Iterable
from typing import Protocol


class SSTable[K, V]:
    
    def __init__(self, storage:DiskStorage[K, V], max_num_retention:int):
        self.storage = storage
        self.max_num_retention = max_num_retention
        self._data = dict[K, V]()
        self._deleted = set()
    
    def get(self, k:K):
        if k in self._deleted:
            return 

        data = self._data
        if k not in data:
            value, = self.storage.get([k]).values()
        else:
            value = data[k]
        
        return value
    
    def set(self, k:K, v:V):
        self._data[k] = v
        
        if k in self._deleted:
            self._deleted.remove(k)

        if len(self._data) >= self.max_num_retention:
            self.storage.put(self._data.items())
            self._data = {}
    
    def delete(self, key:K):
        self._data.pop(key, None)
        self._deleted.add(key)
        
        if len(self._deleted) > self.max_num_retention:
            self.storage.delete(self._deleted)
            self._deleted = set()
    
    def multi_get(self, *keys:K):
        return self.storage.get(keys)
    
    def dump(self):
        if len(self._data) > 0:
            self.storage.put(self._data.items())
            self._data = {}


class DiskStorage[K, V](Protocol):
    
    def put(self, data:Iterable[tuple[K, V]]) -> None:...
    
    def delete(self, data:Iterable[K]) -> None:...
    
    def get(self, data:Iterable[K]) -> dict[K, V|None]:...
