import networkx as nx
import inspect

from typing import Hashable
from pathlib import Path
from warnings import warn
from ..types import Node
from ..links import Link


class Context:
    
    def __init__(self, graph:nx.MultiDiGraph=None, name:Hashable=None):        
        if name is None:
            caller = inspect.stack()[1][0]
            caller = inspect.getmodule(caller)
            path = Path(caller.__file__)
            parent_path = path.parent
            name = parent_path.name
        
        graph = graph if graph is not None else nx.MultiDiGraph()
        graph.add_node(name, type=Node.CONTEXT)

        self.name = name
        self.graph = graph
            
    def add_dependency(self, name, value, as_singleton=False):
        assert as_singleton or callable(value), 'dependency should be callable'
        
        node_id = self.node_id(name)
        if name in self:
            warn(f'{name} is already registered for context {self.name}, overwriting it.')
            neighbors = [*self.graph.neighbors(node_id)]
            self.graph.remove_edges_from([n for n in neighbors])
        
        if as_singleton:
            self.graph.add_node(node_id, type=Node.SINGLETON, value=value)    
        else:
            self.graph.add_node(node_id, type=Node.INITATOR, value=value)
            
            parameters = inspect.signature(value).parameters
            for arg_name, p in parameters.items():
                if arg_name != 'self':
                    arg_id = self.node_id(arg_name)
                    attrs = {}
                    if p.annotation is not inspect._empty:
                        attrs['annotation'] = p.annotation

                    self.graph.add_node(arg_id, **attrs)
                    self.graph.add_edge(node_id, arg_id, Link.DEPEND_ON)
                    
                    if p.default is not inspect.Parameter.empty:
                        self.graph.add_node(arg_id, type=Node.SINGLETON, value=p.default)

        self.graph.add_edge(self.name, node_id, Link.CONTAINS)
        for n in self.graph.neighbors(node_id):
            self.graph.add_edge(node_id, n, Link.CONTAINS)
        return self

    def duplicate(self, current_name:str, new_name:str):        
        assert current_name in self, 'current name must be in dep graph'
        assert new_name not in self, 'new name must not be in dep graph'
        
        current_node = self.node_id(current_name)
        new_node = self.node_id(new_name)
        
        current_graph = self.graph        
        node_attr = current_graph.nodes[current_node]
        neighbors = [*current_graph.successors(current_node)]
        current_graph.add_node(new_node, **node_attr)
        for n in neighbors:
            current_graph.add_edge(new_node, n)
        
        return self

    def __contains__(self, node:str):
        return (self.name, node) in self.graph
    
    def node_id(self, node:str):
        return self.name, node
