from typing import overload, Self


class PositionPath:
    
    def __init__(self, raw_path:list[tuple[int, str]], scores:dict[str, float]):        
        self._raw = raw_path
        self._scores = scores

    def offset(self, i:int):
        return self._raw[i][0]
    
    def token(self, i:int):
        return self._raw[i][1]

    def score(self, i:int):
        token = self.token(i)
        return self._scores[token]

    @overload
    def __getitem__(self, idx:int) -> tuple[int, str]:...
    
    @overload
    def __getitem__(self, idx:slice) -> Self:...
    
    def __getitem__(self, idx:int|slice):
        if isinstance(idx, int):
            return self._raw[idx]
        elif isinstance(idx, slice):
            return PositionPath(self._raw[idx], self._scores)

    def __len__(self):
        return len(self._raw)

    def __iter__(self):
        for n in self._raw:
            yield n

    def __repr__(self):
        return repr(self._raw)
