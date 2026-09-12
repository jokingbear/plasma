
import networkx as nx

from typing import cast

from ..accessor import Accessor


class DataGraph(nx.DiGraph):
    
    def __init__(self, accessor:Accessor):
        assert Accessor.get_parent(accessor) is None
        super().__init__()
        
        self.root = accessor
        _build_graph(self, accessor)

    @property
    def leaves(self):
        for n in self:
            if self.out_degree(n) > 0:
                continue
                
            yield cast(Accessor, n)


def _build_graph(g:nx.DiGraph, a:Accessor):
    g.add_node(a, value=Accessor.get_value(a))
    g.add_edges_from((a, c) for c in Accessor.get_children(a))
    
    for c in Accessor.get_children(a):
        _build_graph(g, c)
