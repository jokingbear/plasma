from typing import get_args, get_origin

from ..inquirer import is_data_model, is_list
from ..field import Field


class FieldParser[T]:
    
    def __init__(self, cls:type[T]):
        assert is_data_model(cls), f'{cls} does not have model decorator'
        self.cls = cls
    
    def from_fields(self, fields:dict[Field, object]) -> T:
        data = {}
        for field in fields:
            resolve(fields, field, data)
        
        return self._from_dict(data)

    def _from_dict(self, data:dict[str, object]):
        args = _Args(self.cls, data)
        return self.cls(**args)


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
            if is_data_model(field_type) and not isinstance(value, field_type):
                assert isinstance(value, dict), 'model must have dict value'
                field_value = FieldParser(field_type)._from_dict(value)
            
            elif is_list(field_type):
                origin = get_origin(field_type)
                if origin is not None:
                    field_type, *_ = get_args(field_type)

                if is_data_model(field_type):
                    field_value = []
                    for v in value:
                        if isinstance(v, field_type):
                            field_value.append(v)
                        elif isinstance(v, dict):
                            field_value.append(FieldParser(field_type)._from_dict(v))
                        else:
                            raise ValueError(f'{v} is not of type {field_type} or dict')

        self[field_name] = field_value
