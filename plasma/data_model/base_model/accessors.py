import re

from .inquirer import is_list, accessors, is_data_model


class AccessorMap:
    
    def __init__(self, cls:type):
        assert is_data_model(cls), f'{cls} is not a data model'
        
        self._accessors = accessors(cls)
    
    def from_dict(self, data:dict[str, object]):
        return Accessor(data)
    
    def to_dict(self, accessors:dict[str, object]):
        return MappedDict(accessors)


class Accessor(dict[str, object]):
    
    def __init__(self, data:dict[str, object]):
        super().__init__()
        
        self.__update(None, data)
        
    def __update(self, key, value):
        if isinstance(value, dict):
            for k, v in value.items():
                next_key = k if key is None else f'{key}.{k}'
                self.__update(next_key, v)
        elif is_list(type(value)):
            for i, v in enumerate(value):
                self.__update(f'{key}.{i}', v)
        else:
            self[key] = value


class MappedDict(dict[str, object]):
    
    def __init__(self, accessors:dict[str, object]):
        super().__init__()
        
        for k, v in accessors.items():
            self.__update(k, v)
    
    def __update(self, key, value):
        components = key.split('.')
        container:dict|list = self
        for i, c in enumerate(components[:-1]):
            next_c = components[i + 1]
            if re.search(r'^\d+$', next_c) is not None:
                next_c = int(next_c)
                current:list = container.setdefault(c, [])
            elif re.search(r'^\d+$', c) is not None:
                c = int(c)
                if len(container) <= c:
                    container.extend([{}] * (c - len(current) + 1))
                
                current = container[c]
            else:
                current = container.setdefault(c, {})
            
            container = current
            
        *_, attr = components
        if re.search(r'^\d+$', attr) is not None:
            attr = int(attr)

        container[attr] = value
