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
    


def resolve(fields_values:dict[Field, object], field:Field, results:dict):
    _, *accessors, name = field.context
    temp_dict = results
    for a in accessors:
        if a not in temp_dict:
            temp_dict[a] = {}
        temp_dict = temp_dict[a]
    
    temp_dict[name] = fields_values[field]