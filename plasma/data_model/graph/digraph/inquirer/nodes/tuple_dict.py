class TupleDict:
    
    def __init__(self, names:list, values:list):
        self._names = names
        self._values = values
        
        self._name_arg_map = {n: i for i, n in enumerate(names)}
    
    def rename(self, old_name, new_name):
        current_arg = self._name_arg_map[old_name]
        self._names[current_arg] = new_name
        self._name_arg_map[new_name] = current_arg
        del self[old_name]

    def update(self, name, value):
        self._names.append(name)
        self._values.append(value)
        self._name_arg_map[name] = len(self._names) - 1
    
    def keys(self):
        return self._names
    
    def __contains__(self, key):
        return key in self._name_arg_map
    
    def __iter__(self):
        for v in self._values:
            yield v
    
    def __getitem__(self, key:int|object):
        if isinstance(key, int):
            value_arg = key
        else:
            value_arg = self._name_arg_map[key]
            
        return self._values[value_arg]
    
    def __getattribute__(self, name):
        if name in super().__getattribute__('_name_arg_map'):
            return self[name]
        else:
            return object.__getattribute__(self, name)
    
    def __len__(self):
        return len(self._values)

    def __repr__(self):
        components = []
        for name, value in zip(self._names, self._values):
            components.append(f'{name}={value}')
        return '(' + ', '.join(components) + ')'
