import re


def accessor2struct(struct_schema, accessors:dict[str, object]):
    results = {}
    for k, v in accessors.items():
        components = k.split('.')
        container = results
        container_struct = struct_schema
        for c in components:
            struct_key = c
            if re.search(r'^\d+$', c) is not None:
                c = int(c)
                struct_key = 0
                
                if len(container) <= c:
                    container.extend([{}] * (c - len(container) + 1))

                current_value = container[c]
            elif isinstance(container_struct[c], list):
                current_value = container.setdefault(c, [])
            elif isinstance(container_struct[c], dict):
                current_value = container.setdefault(c, {})
            else:
                current_value = container.setdefault(c, v)
            
            container = current_value
            container_struct = container_struct[struct_key]
    
    return results


class struct2accessor(dict):
    
    def __init__(self, struct_schema:dict, struct:dict):
        super().__init__()
        
        for k, v in struct.items():
            self.__update(struct_schema[k], k, v)    

    def __update(self, schema, key, value):
        if isinstance(schema, list):
            for i, v in enumerate(value):
                self.__update(schema[0],f'{key}.{i}', v)
        elif isinstance(schema, dict) and value is not None:
            for k, v in value.items():
                self.__update(schema[k], f'{key}.{k}', v)
        else:
            self[key] = value
