import pandas as pd
import re

from typing import Callable


class ObjectInquirer:
    
    def __init__(self):        
        self._type_accessor = {
            pd.DataFrame: lambda frame, i: frame.iloc[i],
            pd.Series: lambda s, k: s.loc[k]
        }
    
    def query(self, obj, chain_attr:str):
        attr_names = chain_attr.split('.')
        for n in attr_names:
            obj_type = type(self.obj)
            if re.search(r'^\d+$', n):
                n = int(n)

            if obj_type in self._type_accessor:
                obj = self._type_accessor[obj_type](obj, n)
            elif isinstance(obj, (list, dict, tuple)):
                obj = obj[n]
            else:
                obj = getattr(obj, n)
                
        return obj

    def register_type(self, t:type, func:Callable[[object, int|str], object]):
        self._type_accessor[t] = func
