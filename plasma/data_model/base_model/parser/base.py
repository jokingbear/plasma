import re

from typing import Callable, get_args

from ..inquirer import is_data_model, is_list
from ..schemas import AccessorSchema, StructSchema, struct2accessor, accessor2struct
from ..field import Field
from ....functional import ReadableClass


class Parser[T](ReadableClass):
    
    def __init__(self, cls:type[T], type_parser:dict[type, Callable[[object], object]]):
        super().__init__()
        
        accessor_schema = AccessorSchema(cls)
        struct_schema = StructSchema(accessor_schema)
        
        self.cls = cls
        self._struct_schema = struct_schema
        self._accessor_schema = accessor_schema
        self._type_parser = type_parser
    
    def from_accessors(self, accessors:dict[str, object]) -> T:
        parsed_accessors = {}
        for k, v in accessors.items():
            schema_key = re.sub(r'\.\d+', '.@idx', k)
            schema_type = self._accessor_schema[schema_key].cls
            parser = self._type_parser.get(schema_type, lambda x:x)
            try:
                parsed_accessors[k] = parser(v)
            except Exception as e:
                error = ValueError(k, v)
                error.add_note(f'error parsing {v} at {k}')
                raise error from e
        
        struct = accessor2struct(self._struct_schema, parsed_accessors)
        return _construct(self.cls, struct)
    
    def from_struct(self, struct:dict) -> T:
        accessors = struct2accessor(self._struct_schema, struct)
        return self.from_accessors(accessors)


def _construct(cls:type, struct):
    if is_list(cls):
        if struct is None:
            struct = []
        
        contained_type = get_args(cls)
        if len(contained_type) > 0:
            return [_construct(contained_type[0], s) for s in struct]
        else:
            return struct
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


class _Args(dict[str, object]):
    
    def __init__(self, root_type:type, data:dict[str, object]):
        super().__init__()
        
        for field_name, field_type in root_type.__annotations__.items():
            self.__update(field_name, field_type, data.get(field_name))
    
    def __update(self, field_name, field_type:type, value):
        field_value = value
        if value is not None:
            if hasattr(field_type, MODEL_FLAG) and not isinstance(value, field_type):
                assert isinstance(value, dict), 'model must have dict value'
                field_value = ModelConstructor(field_type).from_dict(value)
            
            elif isinstance(value, (list, tuple)):
                origin = get_origin(field_type)
                if origin is not None:
                    field_type, *_ = get_args(field_type)

                if hasattr(field_type, MODEL_FLAG):
                    field_value = []
                    for v in value:
                        if isinstance(v, field_type):
                            field_value.append(v)
                        elif isinstance(v, dict):
                            field_value.append(ModelConstructor(field_type).from_dict(v))
                        else:
                            raise ValueError(f'{v} is not of type {field_type} or dict')

        self[field_name] = field_value