from typing import Iterable


class DualDict[S, T]:
    
    def __init__(self, iterable:Iterable[tuple[S, T]]):
        source_target_map = dict[S, T]()
        target_source_map = dict[T, S]()
        for s, t in iterable:
            source_target_map[s] = t
            target_source_map[t] = s
        
        self._st_map = source_target_map
        self._ts_map = target_source_map
    
    @property
    def source_inquirer(self):
        return Mapping(self._ts_map)
    
    @property
    def target_inquirer(self):
        return Mapping(self._st_map)
    
    def __repr__(self):
        lines = [f'{s} - {t}' for s, t in self._st_map.items()]
        return '\n'.join(lines)
    

class Mapping[K, V]:
    
    def __init__(self, data:dict[K, V]):
        self._data = data
    
    def get(self, key:K, default=None):
        return self._data.get(key, default)
    
    def keys(self):
        return self._data.keys()
    
    def items(self):
        return self._data.items()
    
    def values(self):
        return self._data.values()
    
    def __getitem__(self, key):
        return self._data[key]
    
    def __contains__(self, item:K):
        return item in self._data

    def __iter__(self):
        for k in self._data:
            yield k
