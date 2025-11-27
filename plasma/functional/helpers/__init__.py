from .utils import partials, auto_map, chain
from warnings import deprecated


@deprecated('this class is deprecated, use auto_map instead')
def auto_map_func(func):
    return auto_map(func)
