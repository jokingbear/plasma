from typing import Callable

from .accessor import AccessorState
from .struct import StructState
from ..inquirer import is_data_model
from ..schemas import schema
from ....functional import ReadableClass


class Serializer[T](ReadableClass):
    
    def __init__(self, cls:type[T], 
                 sub_serializers:dict[type, Callable]={},
                 expand_none=False):
        super().__init__()

        assert is_data_model(cls)
        
        self._schema = schema(cls)
        self._type_serializer = sub_serializers
        self.expand_none = expand_none
    
    def to_accessors(self, obj:T) -> dict[str, object]:
        r = self._realize(obj)
        return AccessorState(r)
    
    def to_struct(self, obj:T) -> dict[str, object]:
        r = self._realize(obj)
        return StructState(r)
    
    def _realize(self, obj):
        r = self._schema.realize(obj, self.expand_none)
        
        for k in r.endpoints:
            value = r.value(k)
            serializer = self._type_serializer.get(type(value), lambda v:v)
            try:
                value = serializer(value)
            except Exception as e:
                error = ValueError(value)
                accessor = '.'.join(str(a) for a in k)
                error.add_note(f'error serializing field {accessor}')
                raise error from e

            r.mutate(k, value)
            
        return r
