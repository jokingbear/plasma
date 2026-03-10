from typing import Callable

from .base2 import MODEL_FLAG
from ...functional import AutoPipe


class Parser(AutoPipe[[object], object]):
    
    def __init__(self):
        super().__init__()
        self._type_solver = dict[type, Callable[[object], object]]()
    
    def run(self, data):
        data_cls = type(data)
        results = data
        if data_cls in self._type_solver:
            results = self._type_solver[data_cls](data)
        elif hasattr(type(data), MODEL_FLAG):
            results = {}
            for a in type(data).__annotations__:
                value = getattr(data, a)
                value = self.run(value)
                results[a] = value

        elif isinstance(data, (tuple, list)):
            results = [self.run(v) for v in data]
        elif isinstance(data, dict):
            results = {self.run(k): self.run(v) for k, v in data.items()}

        return results
    
    def register_parser[T](self, t:type[T], parser:Callable[[T], object]):
        self._type_solver[t] = parser
        
        return self
