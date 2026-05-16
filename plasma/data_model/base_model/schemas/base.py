from functools import cached_property
from .representation import Representation
from .realization import Realization


class Schema:
    
    def __init__(self, cls:type):
        self.rep = Representation(cls)
        
    @cached_property
    def fields(self):
        return [n for n in self.rep.nodes if self.rep.out_degree(n) == 0]

    def realize(self, obj, expand_none=False):
        return Realization(self.rep, obj, expand_none)
    
    def real_to_rep(self, real_node):
        if real_node == self.rep.root:
            return real_node
        else:
            rep_node = tuple('@idx' if isinstance(a, int) 
                             else a for a in real_node)
            return rep_node
    
    def __repr__(self):
        return repr(self.rep)
