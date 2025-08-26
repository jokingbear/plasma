import networkx as nx

from typing import Hashable, overload
from .types import Node
from .links import Link


class ContextGraph:
    
    def __init__(self, backend:nx.DiGraph=None):
        self.backend = backend if backend is not None else nx.DiGraph()
    
    def __contains__(self, *args):
        assert len(args) < 3
        if len(args) == 1:
            node_id = args[0]
        else:
            node_id = tuple(args)
            
        return node_id in self.backend

    # add/update
    def add_context(self, name:Hashable):
        self.backend.add_node(name, type=Node.CONTEXT)

    def add_node(self, context:Hashable, name:Hashable, **attrs):
        node_id = context, name
        self.backend.add_node(node_id, **attrs)
        self.backend.add_edge(context, node_id, type=Link.CONTAINS)
        
        if context not in self.backend:
            self.add_context(context)
    
    def add_edge(self, head:tuple[Hashable, Hashable], tail:tuple[Hashable, Hashable], link=Link.DEPEND_ON):
        self.backend.add_edge(head, tail, type=link)

    # get
    def __getitem__(self, node_id) -> dict:
        return self.backend.nodes[*node_id]

    @property
    def contexts(self):
        for n, ntype in self.backend.nodes(data='type'):
            if ntype is Node.CONTEXT:
                yield n

    def nodes(self, context:Hashable, *data):
        for n in self.backend.successors(context):
            attrs = self.backend.nodes[n]
            picked_attrs = tuple(attrs[d] for d in data)
            yield n, picked_attrs
    
    def successors(self, context:Hashable, name:Hashable, *data, link=Link.CONTAINS):
        node_id = context, name
        for _, t, rel in self.backend.out_edges(node_id, data='type'):
            if link is None or rel in link:
                attrs = self[*t]
                picked_attrs = tuple(attrs[d] for d in data)
                yield t, picked_attrs
    
    def predecessors(self, context:Hashable, name:Hashable, *data, link=Link.CONTAINS):
        node_id = context, name
        for h, _, rel in self.backend.in_edges(node_id, data='type'):
            if link is None or rel in link:
                attrs = self.backend.nodes[h]
                picked_attrs = tuple(attrs[d] for d in data)
                yield h, picked_attrs

    def in_degree(self, context:Hashable, name:Hashable, link=Link.CONTAINS):
        nodes = [*self.predecessors(context, name, link=link)]
        return len(nodes)
    
    def out_degree(self, context:Hashable, name:Hashable, link=Link.CONTAINS):
        nodes = [*self.successors(context, name, link=link)]
        return len(nodes)

    def type(self, context:Hashable, name: Hashable):
        return self.backend.nodes[(context, name)]['type']
    
    # delete
    def remove_node(self, context:Hashable, name:Hashable):        
        node_id = context, name
        self.backend.remove_node(node_id)
    
    def remove_edge(self, head:tuple[Hashable, Hashable], tail:tuple[Hashable, Hashable],):
        self.backend.remove_edge(head, tail)
