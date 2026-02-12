class TupleDict:
    
    def __init__(self, names:tuple, values:tuple):
        self.__names = names
        self.values = values
        
        name_arg_map = {n: i for i,n  in enumerate(names)}
        self._name_arg_map = name_arg_map
    
    @property
    def items(self):
        return self._dict.items()

    def update(self, new_names, new_values):
        return TupleDict(
            [*self.__names, *new_names],
            [*self.values, *new_values]
        )
    
    def keys(self):
        for n in self.__names:
            yield n
    
    def __getitem__(self, name):
        return self.values[self._name_arg_map[name]]
    
    def __iter__(self):
        for v in self.values:
            yield v

    def __len__(self):
        return len(self.__names)

    def __getattr__(self, name):
        if name in self._name_arg_map:
            return self[name]
        else:
            return super().__getattr__(name)
