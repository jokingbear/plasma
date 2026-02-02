import pandas as pd

from typing import Callable


class EmptyResult:...


class ObjectInquirer:
    
    def __init__(self, obj):
        self.obj = obj
                
        self._type_accessor = {
            pd.DataFrame: lambda frame, i: frame.iloc[int(i)],
            pd.Series: lambda s, k: s.loc[k]
        }
    
    def get(self, chain_attr:str, default=None):
        attr_names = chain_attr.split('.')
        obj = self.obj
        for n in attr_names:
            obj_type = type(obj)

            qresult = EmptyResult
            if obj_type in self._type_accessor:
                qresult = self._type_accessor[obj_type](obj, n)
            elif isinstance(obj, (list, tuple)):
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

    def select(self, attrs, default=None):
        return TupleDict(attrs, [self.get(a, default) for a in attrs])
    
    def register_type[T](self, t:type[T], func:Callable[[T, str], object]):
        self._type_accessor[t] = func


class TupleDict:
    
    def __init__(self, 
                names:tuple, 
                values:tuple
            ):
        
        self._dict = {n: v for n, v in zip(names, values)}
        self._tuple = values
    
    @property
    def selectors(self):
        for n in self._dict:
            yield n
    
    @property
    def items(self):
        return self._dict.items()
    
    @property
    def values(self):
        return self._tuple
    
    def __getitem__(self, name):
        return self._dict[name]
    
    def __iter__(self):
        for v in self._tuple:
            yield v
