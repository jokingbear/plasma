import networkx as nx

from functools import cached_property
from typing import Sequence
from .repr import Repr
from ..representation import Representation


class Realization(nx.DiGraph):
    
    def __init__(self, rep:Representation, obj, expand_none=False):
        super().__init__()

        root = rep.root
        self.add_node(root, value=obj)
        self.__update(rep, root, root, obj, expand_none)
        self.root = root
        
    def __update(self, rep:Representation, rep_node, real_node, value, expand_none):
        if value is None and not expand_none:
            return

        for s in rep.successors(rep_node):
            if s[-1] == '@idx':
                assert isinstance(value, Sequence) or value is None, f'expect Sequence at {'.'.join(str(a) for a in rep_node)}'
                value = value or []
                self.add_node(real_node, value=value)
                for i, v in enumerate(value):
                    next_real_node = (*real_node, i)
                    self.add_node(next_real_node, value=v)
                    self.add_edge(real_node, next_real_node)
                    self.__update(rep, s, next_real_node, v, expand_none)
            else:
                next_real_node = (*real_node, s[-1])
                self.add_edge(real_node, next_real_node)
                
                next_value = getattr(value, s[-1], None)
                self.add_node(next_real_node, value=next_value)
                self.__update(rep, s, next_real_node, next_value, expand_none)

    def value(self, node):
        if node not in self:
            return None

        return self.nodes[node]['value']
    
    @cached_property
    def endpoints(self):
        return [n for n in self if self.out_degree(n) == 0]

    def mutate(self, node, value):
        self.add_node(node, value=value)
    
    def __repr__(self):
        return Repr(self)(self.root)
