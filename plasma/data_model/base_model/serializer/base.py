from typing import Callable

from .accessor import AccessorState
from ..inquirer import is_data_model
from ..schemas import AccessorSchema, StructSchema, accessor2struct
from ....functional import ReadableClass


class Serializer[T](ReadableClass):
    
    def __init__(self, cls:type[T], type_serializer:dict[type, Callable]):
        super().__init__()

        assert is_data_model(cls)
        
        accessor = AccessorSchema(cls)
        self._accessor_schema = accessor
        self._struct_schema = StructSchema(accessor)
        self._type_serializer = type_serializer
    
    def to_accessors(self, obj:T) -> dict[str, object]:
        accessor = AccessorState(self._accessor_schema, obj)
        results = {}
        for k, v in accessor.items():
            serializer = self._type_serializer.get(type(v), lambda x:x)
            results[k] = serializer(v)
        return results
    
    def to_struct(self, obj:T) -> dict[str, object]:
        accessors = self.to_accessors(obj)
        return accessor2struct(self._struct_schema, accessors)
    