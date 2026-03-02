class TupleDict:
    
    def __init__(self, names:list, values:list):
        self._names = names
        self._name_value_map = dict(zip(names, values))
    
    def update(self, name, value):
        self._name_value_map[name] = value
        
        if name not in self:
            self._names.append(name)
    
    def keys(self):
        return self._name_value_map.keys()
    
    def __contains__(self, key):
        return key in self._name_value_map
    
    def __iter__(self):
        for v in self._name_value_map.values():
            yield v
    
    def __getitem__(self, key:int|object):
        name = key
        if isinstance(key, int):
            name = self._names[key]
            
        return self._name_value_map[name]
    
    def __getattribute__(self, name):
        if name in super().__getattribute__('_name_value_map'):
            return self[name]
        else:
            return super().__getattribute__(name)
    
    def __len__(self):
        return len(self._names)

    def __repr__(self):
        components = []
        for name, value in zip(self._names, self._values):
            components.append(f'{name}={value}')
        return '(' + ', '.join(components) + ')'
