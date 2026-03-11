from typing import Callable, get_args

from ..inquirer import is_data_model, is_list
from ..schemas import AccessorSchema, StructSchema, struct2accessor, accessor2struct
from ..field import Field
from ....functional import ReadableClass


class Parser[T](ReadableClass):
    
    def __init__(self, cls:type[T]):
        super().__init__()
        
        accessor_schema = AccessorSchema(cls)
        struct_schema = StructSchema(accessor_schema)
        
        self.cls = cls
        self._struct_schema = struct_schema
        self._accessor_schema = accessor_schema
        self.type_parser = dict[type, Callable]()
    
    def register[T](self, cls:type[T], parser:Callable[[T], object]) -> T:
        self.type_parser[cls] = parser
        return self
    
    def from_accessors(self, accessors:dict[str, object]) -> T:
        parsed_accessors = {}
        for k, v in accessors.items():
            parser = self.type_parser.get(type(v), lambda x:x)
            parsed_accessors[k] = parser(v)
        
        struct = accessor2struct(self._struct_schema, parsed_accessors)
        return _construct(self.cls, struct)
    
    def from_struct(self, struct:dict) -> T:
        accessors = struct2accessor(self._struct_schema, struct)
        return self.from_accessors(accessors)
    
    def from_fields(self, fields:dict[Field, object]):
        data = {}
        for field in fields:
            resolve(fields, field, data)
        
        return self.from_dict(data)


def _construct(cls:type, struct):
    if is_list(cls):
        contained_type = next(get_args(cls), None)
        
        if struct is None:
            return []
        elif contained_type is not None:
            return [_construct(contained_type, s) for s in struct]
    elif isinstance(struct, dict) and is_data_model(cls):
        args = {}
        for a, at in cls.__annotations__.items():
            args[a] = _construct(at, struct.get(a))
        
        return cls(**args)
    else:
        return struct


def resolve(fields_values:dict[Field, object], field:Field, results:dict):
    _, *accessors, name = field.context
    temp_dict = results
    for a in accessors:
        if a not in temp_dict:
            temp_dict[a] = {}
        temp_dict = temp_dict[a]
    
    temp_dict[name] = fields_values[field]
