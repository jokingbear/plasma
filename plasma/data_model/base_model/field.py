from warnings import warn
from copy import copy


class Field:
    
    def __init__(self, context:tuple, cls:type):
        self.context = context
        self.cls = cls
    
    @property
    def accessor(self) -> str:
        return '.'.join(str(c) for c in self.context[1:])
    
    def is_abstract(self):
        return '@' in self.accessor
    
    def __repr__(self):
        type_str = self.context[0].__name__
        return f'{type_str}.{self.accessor}:{self.cls}'
    
    def _prepend(self, context:tuple):
        self.context = tuple([*context, self.context[1:]])
        return self
    
    def _update(self, arg:int, new_context):
        context = [*self.context]
        context[arg] = new_context
        new_field = copy(self)
        new_field.context = context
        return new_field


class Composite(Field):
    
    def __init__(self, context, cls, sub_fields:dict[str, Field]):
        super().__init__(context, cls)

        for name, field in sub_fields.items():
            setattr(self, name, field)
            
        self.sub_fields = sub_fields.values()


class List(Composite):
    
    def __init__(self, context, cls, sub_fields):
        super().__init__(context, cls, sub_fields)
    
    def __getitem__(self, idx):
        assert isinstance(idx, int)
        
        if idx > 0:
            warn('any index different from 0 is meaningless because this is just a symbolic reference')
