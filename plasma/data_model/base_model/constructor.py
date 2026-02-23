from .field import Field, Composite


class ModelConstructor:
    
    def from_fields[T](self, cls:type[T], fields:dict[Field|Composite, object]):
        data = {}
        for field in fields:
            resolve(fields, field, data)
        
        return self.from_dict(cls, data)

    def from_dict[T](self, cls:type[T], data:dict[str, object]):
        args = {}
        for field_name, field_value in data.items():
            annotation = cls.__annotations__[field_name]
            if hasattr(annotation, '__data_model'):
                field_value = self.from_dict(annotation, field_value)
            
            args[field_name] = field_value
            
        return cls(**args)


def resolve(fields_values:dict[Field|Composite, object], field:Field|Composite, results:dict):
    if isinstance(field, Composite):
        for sub_field in field.sub_fields:
            resolve(fields_values, sub_field, results)
    else:
        _, *accessors, name = field.context
        
        temp_dict = results
        for a in accessors:
            if a not in temp_dict:
                temp_dict[a] = {}
            temp_dict = temp_dict[a]

        temp_dict[name] = fields_values.get(field, None)
