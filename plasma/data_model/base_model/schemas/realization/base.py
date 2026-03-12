import networkx as nx

from .repr import Repr
from ..representation import Representation


class Realization(nx.DiGraph):
    
    def __init__(self, rep:Representation, obj, expand_none=False):
        super().__init__()

        root = rep.root
        self.__update(rep, root, root, obj, expand_none)
        self.root = root
        
    def __update(self, rep:Representation, rep_node, real_node, value, expand_none):
        self.add_node(real_node, value=value)
        
        if value is not None or expand_none:
            for s in rep.successors(rep_node):
                if s[-1] == '@idx':
                    value = value or []
                    assert isinstance(value, (tuple, list)), f'expect tuple or list at {'.'.join(str(a) for a in real_node)}'
                    for i, v in enumerate(value):
                        next_real_node = (*real_node, i)
                        self.add_edge(real_node, next_real_node)
                        self.__update(rep, s, (*real_node, i), v, expand_none)
                else:
                    next_real_node = (*real_node, s[-1])
                    self.add_edge(real_node, next_real_node)
                    
                    next_value = getattr(value, s[-1], None)
                    self.__update(rep, s, next_real_node, next_value, expand_none)

    def value(self, node):
        return self.nodes[node]['value']
    
    @property
    def endpoints(self):
        for n in self:
            if self.out_degree(n) == 0:
                yield n

    def mutate(self, node, value):
        self.add_node(node, value=value)
    
    def __repr__(self):
        return Repr(self).run()
