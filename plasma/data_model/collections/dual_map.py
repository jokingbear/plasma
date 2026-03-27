from typing import Iterable, Hashable, Literal
from collections import defaultdict


class DualMap[S:Hashable, T:Hashable]:
    
    def __init__(self, iterable:Iterable[tuple[S, T]]):
        source_target_map = defaultdict[S, list[T]](list)
        target_source_map = defaultdict[T, list[S]](list)
        for s, t in iterable:
            source_target_map[s].append(t)
            target_source_map[t].append(s)
        
        self._st_map = source_target_map
        self._ts_map = target_source_map
    
    def get_sources(self, target:T, default:S|Literal['empty']=None):
        if default == 'empty':
            defaults = []
        else:
            defaults = [default]

        return tuple(self._ts_map.get(target, defaults))
    
    def get_targets(self, source:S, default:S|Literal['empty']=None):
        if default == 'empty':
            defaults = []
        else:
            defaults = [default]

        return tuple(self._st_map.get(source, defaults))
    
    @property
    def sources(self):
        return tuple(self._st_map)
    
    @property
    def targets(self):
        return tuple(self._ts_map)
        
    def __repr__(self):
        lines = []
        for s, ts in self._st_map.items():
            lines.append(f'{s}:')
            if len(ts) == 1:
                lines[-1] += f'{ts[0]}'
            else:
                lines.extend(f'  {t}' for t in ts)
            lines.append('=' * 20)

        return '\n'.join(lines)
