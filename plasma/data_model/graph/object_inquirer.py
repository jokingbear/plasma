import pandas as pd
import re

from typing import Callable


class EmptyResult:...


class ObjectInquirer:
    
    def __init__(self):        
        self._type_accessor = {
            pd.DataFrame: lambda frame, i: frame.iloc[i],
            pd.Series: lambda s, k: s.loc[k]
        }
    
    def get(self, obj, chain_attr:str, default=None):
        attr_names = chain_attr.split('.')
        for n in attr_names:
            obj_type = type(obj)
            if re.search(r'^\d+$', n):
                n = int(n)
            
            qresult = EmptyResult
            if obj_type in self._type_accessor:
                qresult = self._type_accessor[obj_type](obj, n)
            elif isinstance(obj, (list, tuple)):
                qresult = obj[n]
            elif isinstance(obj, dict):
                qresult = obj.get(n, qresult)
            elif hasattr(obj, n):
                qresult = getattr(obj, n)
            
            obj = qresult
            if obj is EmptyResult:
                obj = default
                break
                
        return obj

    def register_type(self, t:type, func:Callable[[object, int|str], object]):
        self._type_accessor[t] = func
