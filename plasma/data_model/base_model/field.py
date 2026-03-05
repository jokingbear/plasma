class Field:
    
    def __init__(self, context):
        self.context = context
    
    def __repr__(self):
        type_str = self.context[0].__name__
        return type_str + '.' + '.'.join(str(c) for c in self.context[1:])


class Composite(Field):
    
    def __init__(self, context, sub_fields:dict[str, Field]):
        super().__init__(context)

        for name, field in sub_fields.items():
            setattr(self, name, field)
            
        self.sub_fields = sub_fields.values()
