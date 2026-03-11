from typing import Callable

from .accessor import AccessorState
from ..inquirer import is_data_model
from ..schemas import AccessorSchema, StructSchema, accessor2struct
from ....functional import ReadableClass


class Serializer[T](ReadableClass):
    
    def __init__(self, cls:type[T]):
        super().__init__()

        assert is_data_model(cls)
        
        self._accessor_schema = AccessorSchema(cls)
        self._struct_schema = StructSchema(cls)

        self.type_serializer = dict[type, Callable]()
        
    def register[T](self, cls:T, serializer:Callable[[T], object]):
        self.type_serializer[cls] = serializer
        
        return self
    
    def to_accessors(self, obj:T) -> dict[str, object]:
        accessor = AccessorState(self._accessor_schema, obj)
        results = {}
        for k, v in accessor.items():
            serializer = self.type_serializer.get(type(v), lambda x:x)
            results[k] = serializer(v)
        return results
    
    def to_struct(self, obj:T) -> dict[str, object]:
        accessors = self.to_accessors(obj)
        return accessor2struct(self._struct_schema, accessors)
    