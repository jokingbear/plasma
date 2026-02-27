from .field import Field
from .base2 import MODEL_FLAG


class ModelConstructor[T]:
    
    def __init__(self, cls:type[T]):
        assert hasattr(cls, MODEL_FLAG), f'{cls} does not have model decorator'
        self._cls = cls
    
    def from_fields(self, fields:dict[Field, object]):
        data = {}
        for field in fields:
            resolve(fields, field, data)
        
        return self.from_dict(data)

    def from_dict(self, data:dict[str, object]):
        args = {}
        for field_name, field_value in data.items():
            annotation = self._cls.__annotations__[field_name]
            if hasattr(annotation, MODEL_FLAG) and isinstance(field_value, dict):
                field_value = ModelConstructor(annotation).from_dict(field_value)
            
            args[field_name] = field_value
            
        return self._cls(**args)


def resolve(fields_values:dict[Field, object], field:Field, results:dict):
    _, *accessors, name = field.context
    temp_dict = results
    for a in accessors:
        if a not in temp_dict:
            temp_dict[a] = {}
        temp_dict = temp_dict[a]
    
    temp_dict[name] = fields_values[field]
