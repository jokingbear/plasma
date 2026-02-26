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
    
    def arg_search(self, input:T):
        sorted_array = self._sorted_data
        arg = len(sorted_array) // 2
        offset = 0
        dist = partials(self._metric, input, pre_apply_before=False)
        counter = 0
        while len(sorted_array) > 0:
            counter += 1
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
        print(f'counter={counter}')
        return offset + arg

    def __getitem__(self, idx:int|slice):
        if isinstance(idx, int):
            return self._sorted_data[idx]
        else:
            return SortedInquirer(
                        self._sorted_data[idx], 
                        self._key, 
                        self._metric
                    )
    
    def __len__(self):
        return len(self._sorted_data)

    def __repr__(self):
        return repr(self._sorted_data)
