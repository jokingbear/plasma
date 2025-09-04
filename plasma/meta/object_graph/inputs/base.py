class Inputs:
    
    def __init__(self, inputs:dict=None):
        inputs = inputs or {}        
        annotations = self.__annotations__
        
        registrators = {}
        for ak, av in annotations.items():
            if ak in inputs:
                value = inputs[ak]
                if issubclass(av, Inputs):
                    assert isinstance(value, dict)
                    setattr(self, ak, av(value))
                elif isinstance(av, type):
                    setattr(self, ak, value)
            elif hasattr(self, ak) and isinstance(getattr(self, ak), Registrator):
                registrators[ak] = getattr(self, ak)
        
        for k, v in registrators.items():
            setattr(self, k, v.func(self))
    
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
    
    def __call__(self, func):
        self.func = func
        return func
