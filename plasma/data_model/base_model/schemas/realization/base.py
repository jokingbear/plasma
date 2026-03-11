import networkx as nx

from .repr import Repr
from ..representation import GraphRepresetation


class Realization(nx.DiGraph):
    
    def __init__(self, rep:GraphRepresetation, obj):
        super().__init__()
        
        self.__update(rep, '', '', obj)
        
    def __update(self, rep:GraphRepresetation, rep_node, real_node, value):
        self.add_node(real_node, value=value)
        
        if value is not None:
            for s in rep.successors(rep_node):
                if s[-1] == '@idx':
                    for i, v in enumerate(value):
                        next_real_node = (*real_node, i)
                        self.add_edge(real_node, next_real_node)
                        self.__update(rep, s, (*real_node, i), v)
                else:
                    next_real_node = (*real_node, s[-1])
                    self.add_edge(real_node, next_real_node)
                    self.__update(rep, s, next_real_node, getattr(value, s[-1]))

    def __repr__(self):
        return Repr(self).run()
