from ..field import Field, Composite, List
from ..inquirer import is_data_model


class AccessorSchema(dict[str, Field]):
    
    def __init__(self, model_cls:type):
        super().__init__()
        
        for a in model_cls.__annotations__:
            self.__update(getattr(model_cls, a))
    
    def __update(self, field:Field):
        if isinstance(field, Composite):
            for f in field.sub_fields.values():
                self.__update(f)
        elif isinstance(field, List) and is_data_model(field.cls):
            accessors = AccessorSchema(field.cls)
            current_accessor = field.accessor + '.@idx.'
            for a, f in accessors.items():
                self[current_accessor + a] = f
        else:
            self[field.accessor] = field
