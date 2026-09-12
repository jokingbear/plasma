from collections.abc import Iterable, Hashable
from warnings import warn

from ...functional import ReadableClass


class BiMap[S:Hashable, T:Hashable](ReadableClass):
    
    def __init__(self, iterable:Iterable[tuple[S, T]]):
        super().__init__()

        source_target_map = dict[S, T]()
        target_source_map = dict[T, S]()
        for s, t in iterable:
            if s in source_target_map:
                warn('detected duplication in source, overwriting data', stacklevel=2)
            
            if t in target_source_map:
                warn('detected duplication in source, overwriting data', stacklevel=2)
            source_target_map[s] = t
            target_source_map[t] = s
        
        self._st_map = source_target_map
        self._ts_map = target_source_map
    
    def get_source(self, target:T, default:S|None=None):
        return self._ts_map.get(target, default)
    
    def get_target(self, source:S, default:T|None=None):
        return self._st_map.get(source, default)
    
    @property
    def sources(self):
        return tuple(self._st_map)
    
    @property
    def targets(self):
        return tuple(self._ts_map)
    
    def _tree(self, tree):
        for s, t in self._st_map.items():
            tree.add(f'{s} - {t}')
        return tree
