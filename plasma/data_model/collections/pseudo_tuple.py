from typing import Self, Sequence, overload


class PseudoTuple[D]:
    
    def __init__(self, data:Sequence[D]):
        self._data = data
    
    def _slice_init(self, sliced_data:Sequence[D]) -> Self:...
    
    @overload
    def __getitem__(self, idx:int) -> D:...
    
    @overload
    def __getitem__(self, idx:slice) -> Self:...
      
    def __getitem__(self, idx):
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
