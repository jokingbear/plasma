class Field:
    
    def __init__(self, context):
        self.context = context
    
    def __repr__(self):
        return '.'.join(str(c) for c in self.context)


class Composite(Field):
    
    def __init__(self, context, sub_fields:dict[str, Field]):
        super().__init__(context)

        for name, field in sub_fields.items():
            setattr(self, name, field)
            
        self.sub_fields = sub_fields.values()

    def __repr__(self):
        return '.'.join(str(c) for c in self.context)
