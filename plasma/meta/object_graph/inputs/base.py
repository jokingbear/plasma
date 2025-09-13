class Inputs:
    
    def __init__(self, inputs:dict=None):
        inputs = inputs or {}        
        annotations = self.__annotations__
        
        for ak, av in annotations.items():
            if ak in inputs:
                value = inputs[ak]
                if issubclass(av, Inputs):
                    assert isinstance(value, dict)
                    setattr(self, ak, av(value))
                elif isinstance(av, type):
                    setattr(self, ak, value)
            elif hasattr(self, ak) and isinstance(getattr(self, ak), Registrator):
                attr = getattr(self, ak)
                attr.set(self, ak)
        
        Registrator.init_prop(self)

    def to_dict(self):
        results = {}
        for k in self.__annotations__:
            if hasattr(self, k):
                value = getattr(self, k)
                if isinstance(value, Inputs):
                    value = value.to_dict()
                
                results[k] = value

        return results


class Registrator:
    __obj_maps = {}
    
    def __call__(self, func):        
        self._func = func
        return func
    
    def set(self, instance:Inputs, prop_name:str):
        prop_func_list = self.__obj_maps.get(id(instance), [])
        prop_func_list.append([prop_name, self._func])
        self.__obj_maps[id(instance)] = prop_func_list
    
    @classmethod
    def init_prop(cls, inputs:Inputs):
        func_maps = {}
        for prop_name, func in cls.__obj_maps.get(id(inputs), []):
            prop_list = func_maps.get(func, [])
            prop_list.append(prop_name)
            func_maps[func] = prop_list
            pass
        
        for f, props in func_maps.items():
            outputs = f(inputs)
            if len(props) == 1:
                setattr(inputs, props[0], outputs)
            else:
                for p, o in zip(props, outputs):
                    setattr(inputs, p, o)
