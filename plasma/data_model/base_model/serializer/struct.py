from ..inquirer import struct


class StructState(dict):
    
    def __init__(self, struct_schema, obj):
        super().__init__()

        if obj is not None:
            for k in struct_schema:
                self.__update(struct, k, obj)
        
    def __update(self, schema, key, obj):
        next_template = schema[key]
        value = getattr(obj, key)
        if isinstance(next_template, dict):
            self[key] = StructState(value)
        elif isinstance(next_template, list):
            assert isinstance(value, (list, tuple)), f'expected list or tuple for {obj} at {key}'
            self[key] = [StructState(v) for v in value]
        else:
            self[key] = value
