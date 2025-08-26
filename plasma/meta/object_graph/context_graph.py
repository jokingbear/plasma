import networkx as nx

from typing import Hashable, overload
from .types import Node
from .links import Link


class ContextGraph:
    
    def __init__(self, backend:nx.MultiDiGraph=None):
        self.backend = backend if backend is not None else nx.MultiDiGraph()
    
    @overload
    def __contains__(self, node:Hashable):
        return node in self.backend
    
    @overload
    def __contains__(self, name:Hashable, context:Hashable):
        return self.node_id(name, context) in self.backend
    
    @overload
    def node_id(self, name:Hashable, context:Hashable):
        node_id = context, name
        return node_id
    
    @overload
    def node_id(self, context:Hashable):
        return context
    
    def node_context_name(self, node_id):
        return node_id

    # add/update
    def add_context(self, name:Hashable):
        self.backend.add_node(name, type=Node.CONTEXT)

    def add_node(self, name:Hashable, context:Hashable, **attrs):
        node_id = self.node_id(context, name)
        self.backend.add_node(node_id, **attrs)
        self.backend.add_edge(name, node_id, Link.CONTAINS)
        
        if name not in self.backend:
            self.add_context(context)
    
    def add_edge(self, head_name:Hashable, head_context:Hashable, 
                tail_name:Hashable, tail_context:Hashable, type=Link.DEPEND_ON):
        hid = self.node_id(head_name, head_context)
        tid = self.node_id(tail_name, tail_context or head_context)
        self.backend.add_edge(hid, tid, type)

    # get
    def __getitem__(self, context:Hashable, name:Hashable) -> dict:
        return self.backend.nodes[self.node_id(context, name)]

    def neighbors(self, name:Hashable, context:Hashable, *data):
        node_id = self.node_id(name, context)
        for n in self.backend.neighbors(node_id):
            attrs = self.backend.nodes[n]
            new_attrs = {d: attrs[d] for d in data}
            yield n, new_attrs
    
    def predecessors(self, name:Hashable, context:Hashable, *data):
        node_id = self.node_id(name, context)
        for n in self.backend.predecessors(node_id):
            attrs = self.backend.nodes[n]
            new_attrs = {d: attrs[d] for d in data}
            yield n, new_attrs
    
    def in_degree(self, name:Hashable, context:Hashable, link_type=Link.CONTAINS):
        edges = [*self.in_edges(name, context, link_type)]
        return len(edges)
    
    def out_degree(self, name:Hashable, context:Hashable, link_type=Link.CONTAINS):
        edges = [*self.out_edges(name, context, link_type)]
        return len(edges)

    def nodes(self, context:Hashable, *data):
        for n in self.backend.successors(context):
            attrs = self.backend.nodes[n]
            picked_attrs = {d: attrs[d] for d in data}
            yield self.node_context_name(n), picked_attrs
    
    def out_edges(self, name:Hashable, context:Hashable, link_type=Link.CONTAINS):
        node_id = self.node_id(name, context)
        for h, _, rel in self.backend.out_edges(node_id, keys=True):
            if link_type is None or link_type == rel:
                yield h
    
    def in_edges(self, name:Hashable, context:Hashable, link_type=Link.CONTAINS):
        node_id = self.node_id(name, context)
        for _, t, rel in self.backend.in_edges(node_id, keys=True):
            if link_type is None or rel in link_type:
                yield self.node_context_name(t)
    
    # delete
    def remove_node(self, name:Hashable, context:Hashable):        
        node_id = self.node_id(name, context)
        self.backend.remove_node(node_id)
        self.backend.remove_edge(context, node_id)
    
    def remove_edge(self, head_name:Hashable, head_context:Hashable, 
                    tail_name:Hashable, tail_context:Hashable, type=Link.DEPEND_ON):
        hid = self.node_id(head_name, head_context)
        tid = self.node_id(tail_name, tail_context)
        self.backend.remove_edge(hid, tid, type)
