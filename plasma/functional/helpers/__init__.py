from .automap import auto_map
from warnings import deprecated
from .partials import partials
from .chain import chain
from .itertools import groupby
from .color_printer import Color


@deprecated('this class is deprecated, use auto_map instead')
def auto_map_func(func):
    return auto_map(func)
