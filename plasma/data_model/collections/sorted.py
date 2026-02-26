from typing import Iterable, Callable
from ...functional import partials

def _identity(x):
    return x


def _abs_diff(x, y):
    return abs(x - y)


def sorted_inquirer[T](data:Iterable[T], 
                       key:Callable[[T], object]=_identity,
                       metric:Callable[[T, T], float]=_abs_diff):
    sorted_list = sorted(data, key=key)
    return SortedInquirer[T](sorted_list, key, metric)


class SortedInquirer[T]:
    
    def __init__(self, 
                sorted_data:list[T], 
                key:Callable[[T], object],
                metric:Callable[[T, T], float]=None
            ):
        super().__init__()
        
        self._sorted_data = sorted_data
        self._key = key
        self._metric = metric
    
    def __getitem__(self, idx:int|slice):
        if isinstance(idx, int):
            return self._sorted_data[idx]
        else:
            return SortedInquirer(
                        self._sorted_data[idx], 
                        self._key, 
                        self._metric
                    )
    
    def arg_search(self, input:T):
        sorted_array = self._sorted_data
        arg = len(sorted_array) // 2
        offset = 0
        dist = partials(self._metric, input, pre_apply_before=False)
        while len(sorted_array) > 0:
            if len(sorted_array) <= 2:
                arg = min(range(len(sorted_array)), key=lambda a: dist(sorted_array[a]))
                break
            elif input < sorted_array[arg]:
                sorted_array = sorted_array[:arg]
                arg = len(sorted_array) // 2
            elif input > sorted_array[arg]:
                sorted_array = sorted_array[arg:]
                offset += arg
                arg = len(sorted_array) // 2
        
        return offset + arg
