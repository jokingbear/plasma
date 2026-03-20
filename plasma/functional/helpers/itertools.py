from typing import Callable, Iterable
from warnings import deprecated

from .color_printer import Color
from ...data_model.collections import groupby as col_groupby

_msg = 'use plasma.data_model.collections.groupby instead'
@deprecated(_msg)
class groupby[K, V](col_groupby[K, V]):
    
    def __init__[D](self,                     
                    data:Iterable[D], 
                    key:Callable[[D], K],
                    selector:Callable[[D], V]=lambda x:x):
        super().__init__(data, key, selector)
        
        print(Color.YELLOW.render(_msg))
