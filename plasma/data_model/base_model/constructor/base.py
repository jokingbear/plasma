from typing import (
    get_origin, get_args, 
    Iterator, Callable
)

from ..field import Field
from ..constants import MODEL_FLAG


class ModelConstructor[T]:
    
    def __init__(self, cls:type[T]):
        assert hasattr(cls, MODEL_FLAG), f'{cls} does not have model decorator'
        self._cls = cls
        self._type_parser = dict[type, Callable[[object], object]]()
    
    def from_fields(self, fields:dict[Field, object]):
        data = {}
        for field in fields:
            resolve(fields, field, data)
        
        return self.from_dict(data)

    def from_dict(self, data:dict[str, object]):
        args = _Args(self._cls, data)
        return self._cls(**args)
    
    def from_accessor(self, data:dict[str, object]):
        pass
    
    def register[T](self, cls:type[T], parser:Callable[[T], object]):
        self._type_parser[cls] = parser
        return self


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
