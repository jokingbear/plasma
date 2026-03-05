from typing import Self


class PseudoTuple[D]:
    
    def __init__(self, data:tuple[D, ...]):
        self._data = data
    
    def _slice_init(self, sliced_data:tuple[D,...]) -> Self:...
    
    def __getitem__(self, idx:int|slice):
        if isinstance(idx, int):
            return self._data[idx]
        else:
            return self._slice_init(self._data[idx])
    
    def __len__(self):
        return len(self._data)
    
    def __iter__(self):
        for d in self._data:
            yield d

    def __repr__(self):
        return repr(self._data)
