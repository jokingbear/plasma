class Field:
    
    def __init__(self, context, cls:type):
        self.context = context
        self.cls = cls
    
    def __repr__(self):
        type_str = self.context[0].__name__
        return type_str + '.' + '.'.join(str(c) for c in self.context[1:])


class Composite(Field):
    
    def __init__(self, context, cls, sub_fields:dict[str, Field]):
        super().__init__(context, cls)

        for name, field in sub_fields.items():
            setattr(self, name, field)
            
        self.sub_fields = sub_fields


class List(Field):
    
    def __init__(self, context, contained_type):
        super().__init__(context, contained_type)
