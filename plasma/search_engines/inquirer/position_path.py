from typing import overload, Self


class PositionPath:
    
    def __init__(self, raw_path:list[tuple[int, str]]):        
        self._raw = raw_path

    def offset(self, i:int):
        return self._raw[i][0]
    
    def token(self, i:int):
        return self._raw[i][1]

    @overload
    def __getitem__(self, idx:int) -> tuple[int, str]:...
    
    @overload
    def __getitem__(self, idx:slice) -> Self:...
    
    def __getitem__(self, idx:int|slice):
        if isinstance(idx, int):
            return self._raw[idx]
        elif isinstance(idx, slice):
            return PositionPath(self._raw[idx])

    def __len__(self):
        return len(self._raw)

    def __iter__(self):
        for n in self._raw:
            yield n

    def __repr__(self):
        return repr(self._raw)
