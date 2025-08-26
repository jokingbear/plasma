import networkx as nx
import inspect

from typing import Hashable
from ..types import Node
from ..links import Link


class Primitive:
    
    def __init__(self, graph:nx.MultiDiGraph=None, name:Hashable=None):                
        graph = graph if graph is not None else nx.MultiDiGraph()
        graph.add_node(name, type=Node.CONTEXT)

        self.name = name
        self._graph = graph
            
    def __contains__(self, node:Hashable):
        return (self.name, node) in self._graph
    
    def node_id(self, name:Hashable):
        return self.name, name
    
    def node_name(self, node_id):
        return node_id[1]
    
    def _add_node(self, name:Hashable, **attrs):
        node_id = self.node_id(name)
        self._graph.add_node(node_id, **attrs)
        self._graph.add_edge(self.name, node_id, Link.CONTAINS)
    
    def _add_edge(self, head, tail, type=Link.DEPEND_ON):
        hid = self.node_id(head)
        tid = self.node_id(tail)
        self._graph.add_edge(hid, tid, type)

    def __getitem__(self, name) -> dict:
        return self._graph.nodes[self.node_id(name)]

    def neighbors(self, name):
        node_id = self.node_id(name)
        deps = [self.node_name(n) for n in self._graph.neighbors(node_id)]
        return deps
    
    def _remove_node(self, name):        
        node_id = self.node_id(name)
        self._graph.remove_node(node_id)
    
    def _remove_edge(self, head, tail, type=Link.DEPEND_ON):
        hid = self.node_id(head)
        tid = self.node_id(tail)
        self._graph.remove_edge(hid, tid, type)

    def in_degree(self, name):
        return self._graph.in_degree(self.node_id(name))
    
    def out_degree(self, name):
        return self._graph.out_degree(self.node_id(name))
