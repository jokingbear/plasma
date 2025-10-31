class Inputs:
    
    def __init__(self, data:dict={}):
        func2reg_maps = dict[object, list[Initiable]]()
        for k, t in type(self).__annotations__.items():
            if t is Initiable:
                registrator = getattr(self, k)
                if registrator.init_func not in func2reg_maps:
                    func2reg_maps[registrator.init_func] = []
                
                func2reg_maps[registrator.init_func].append(registrator)
            elif k in data and issubclass(t, Inputs):
                setattr(self, k, t(data[k]))
            elif k in data:
                setattr(self, k, data[k])
        
        for func, regs in func2reg_maps.items():
            init(self, func, regs)
    
    def __init_subclass__(cls):
        for k, v in cls.__annotations__.items():
            if v is Initiable:
                setattr(cls, k, v(cls, k))
    
    def to_dict(self):
        results = {}
        for k in self.__annotations__:
            if hasattr(self, k):
                value = getattr(self, k)
                if isinstance(value, Inputs):
                    value = value.to_dict()
                
                results[k] = value

        return results


class Initiable:

    def __init__(self, input_cls, key):
        self.cls = input_cls
        self.key = key
        self.init_func = None
        self._value = None
        self.rank = 0
    
    def __get__(self, *_):
        if self._value is None:
            return self
        else:
            return self._value
    
    def __repr__(self):
        return f'{self.cls}.{self.key} = {self.init_func}:{self.rank}'
    
    def __call__(self, init_func):
        self.init_func = init_func
        
        rank = -1
        current_rank_attrname = '__registered_max_rank'
        if hasattr(init_func, current_rank_attrname):
            rank = getattr(init_func, current_rank_attrname)
        rank += 1
        self.rank = rank
        setattr(init_func, current_rank_attrname, rank)
        
        return init_func


def init(obj, func, registrators:list[Initiable]):
    props = func(obj)
    if len(registrators) == 1:
        registrators[0]._value = props
    else:
        for r, p in zip(sorted(registrators, key=lambda r: r.rank), props):
            r._value = p
