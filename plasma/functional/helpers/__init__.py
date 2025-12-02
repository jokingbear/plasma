from .utils import auto_map, chain
from warnings import deprecated
from .partials import partials


@deprecated('this class is deprecated, use auto_map instead')
def auto_map_func(func):
    return auto_map(func)
