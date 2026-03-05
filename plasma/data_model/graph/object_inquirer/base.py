import pandas as pd
import itertools

from typing import Callable, NamedTuple
from ...base_model import Field


class ObjectInquirer:
    
    def __init__(self, obj):
        self.obj = obj
                
        self._type_accessor = {
            pd.DataFrame: lambda frame, i: frame.iloc[int(i)],
            pd.Series: lambda s, k: s.loc[k]
        }
    
    def get(self, chain_attr:str|Field, default=None):
        if isinstance(chain_attr, str):
            attr_names = chain_attr.split('.')
        else:
            attr_names = chain_attr.context[1:]

        obj = self.obj
        for n in attr_names:
            obj_type = type(obj)

            qresult = EmptyResult
            if obj_type in self._type_accessor:
                qresult = self._type_accessor[obj_type](obj, n)
            elif isinstance(obj, (list, tuple)) and not hasattr(obj, '__orig_bases__'):
                qresult = obj[int(n)]
            elif isinstance(obj, dict):
                qresult = obj.get(n, qresult)
            elif hasattr(obj, n):
                qresult = getattr(obj, n)
            
            obj = qresult
            if obj is EmptyResult:
                obj = default
                break
                
        return obj

    def register_type[T](self, t:type[T], func:Callable[[T, str], object]):
        self._type_accessor[t] = func


class EmptyResult:...
