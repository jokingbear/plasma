_sorted = sorted


def _identity[T](x:T) -> T:
    return x


def _abs_diff(x, y):
    return abs(x - y)


def sorted[D, K](
        data:Iterable[D], 
        key:Callable[[D], K]=_identity,
        metric:Callable[[K, K], float]=_abs_diff
    ):
    sorted_list = _sorted(data, key=key)
    return SortedTuple[D, K](sorted_list, key, metric)
