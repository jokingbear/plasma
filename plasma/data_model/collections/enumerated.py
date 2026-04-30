from typing import Iterable, overload, Self


class Enumerated[T]:
    
    def __init__(self, data:Iterable[T]):
        data = tuple(data)
        self._data = data
        self._id2arg = {id(d): i for i, d in enumerate(data)}
    
    def find_arg(self, item:T):
        return self._id2arg.get(id(item), None)
    
    def __contains__(self, item:T):
        return id(item) in self._id2arg
    
    def __len__(self):
        return len(self._data)
    
    @overload
    def __getitem__(self, key:int) -> T:...
    
    @overload
    def __getitem__(self, key:slice) -> Self:...

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._data[key]
        else:
            return Enumerated(self._data[key])

    def __iter__(self):
        yield from self._data
