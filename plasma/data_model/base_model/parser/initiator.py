from typing import Callable
from networkx import DiGraph

from ..schemas import Representation
from ..inquirer import is_data_model


class Initator:
    
    def __init__(self, rep:Representation, data:DiGraph, 
                 real_to_rep:Callable[[object], object]):
        self.rep = rep
        self.data = data
        self.real_to_rep = real_to_rep
        
        state = {}
        for n in data:
            if data.out_degree(n) == 0:
                state[n] = data.nodes[n]['value']

        self._state = state
    
    def run(self):
        self._iterate(self.rep.root)
        return self._state[self.rep.root]
    
    def _iterate(self, real_node):
        if real_node in self._state:
            return
        
        rep_node = self.real_to_rep(real_node)
        origin, args = self.rep.type(rep_node)

        if is_data_model(origin):
            args = {}
            for s in self.data.successors(real_node):
                self._iterate(s)
                args[s[-1]] = self._state[s]
            
            for a in origin.__annotations__:
                if a not in args:
                    args[a] = None
            
            value = origin(**args)
            self._state[real_node] = value
        elif issubclass(origin, (list, tuple)) and len(args) > 0 and is_data_model(args[0]):
            value = []
            for s in self.data.successors(real_node):
                self._iterate(s)
                value.append(self._state[s])
            
            self._state[real_node] = value
