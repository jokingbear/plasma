from .field import Field, Composite, List
from .inquirer import is_data_model


class Accessors(dict[str, Field]):
    
    def __init__(self, model_cls:type):
        super().__init__()
        
        for a in model_cls.__annotations__:
            self.__update(getattr(model_cls, a))
    
    def __update(self, field:Field):
        if isinstance(field, Composite):
            for f in field.sub_fields.values():
                self.__update(f)
        elif isinstance(field, List) and is_data_model(field.cls):
            accessors = Accessors(field.cls)
            current_accessor = field.accessor + '.@idx.'
            for a, f in accessors.items():
                self[current_accessor + a] = f
        else:
            self[field.accessor] = field


class Struct(dict):

    def __init__(self, accessors:Accessors):
        super().__init__()

        for k, v in accessors.items():
            container = self
            components = k.split('.')
            for i, c in enumerate(components):
                if i == len(components) - 1:
                    current = container.setdefault(c, k)
                elif c == '@idx':
                    current = container[0]
                elif components[i + 1] == '@idx':
                    current = container.setdefault(c, [{}])
                else:
                    current = container.setdefault(c, {})
                
                container = current
