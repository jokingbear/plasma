import networkx as nx
import inspect

from typing import Hashable
from pathlib import Path
from warnings import warn
from ..types import Node
from ..context_graph import ContextGraph


class Base:
    
    def __init__(self, graph:ContextGraph, name:Hashable=None):
        if name is None:
            caller = inspect.stack()[1][0]
            caller = inspect.getmodule(caller)
            path = Path(caller.__file__)
            parent_path = path.parent
            name = parent_path.name
            
        graph.add_context(name)
        self.graph = graph
        self.name = name
            
    def add_dependency(self, name:Hashable, value, as_singleton=False):
        assert as_singleton or callable(value), 'dependency should be callable'
        
        graph = self.graph
        if (name, self.name) in graph and graph[name, self.name]['type'] is not Node.LEAF:
            warn(f'{name} is already registered for context {self.name}, overwriting it.')
            self.remove_dependency(name)

        if as_singleton:
            graph.add_node(name, self.name, type=Node.SINGLETON, value=value)
        else:
            graph.add_node(name, self.name, type=Node.INITATOR, value=value)
            
            parameters = inspect.signature(value).parameters
            for arg_name, p in parameters.items():
                if arg_name != 'self':
                    attrs = {}
                    if p.annotation is not inspect._empty:
                        attrs['annotation'] = p.annotation
                    
                    if arg_name not in self:
                        attrs['type'] = Node.LEAF
                    
                    if p.default is not inspect.Parameter.empty:
                        attrs['value'] = p.default

                    graph.add_node(arg_name, self.name, **attrs)
                    graph.add_edge(name, self.name, 
                                   arg_name, self.name)

        return self

    def duplicate(self, current_name:Hashable, new_name:Hashable):        
        assert current_name in self, 'current name must be in dep graph'
        assert new_name not in self, 'new name must not be in dep graph'
               
        graph = self.graph
        node_attrs = graph[current_name, self.name]
        neighbors = graph.neighbors(current_name, self.name)
        self.graph.add_node(new_name, self.name, **node_attrs)
        for n, _ in neighbors:
            context, name = graph.node_context_name(n)
            if context == self.name:
                self.graph.add_edge(new_name, self.name, name, self.name)
        
        return self

    def remove_dependency(self, name:Hashable):
        graph = self.graph
        check_nodes = []
        node_attrs = graph[name, self.name]
        for k in list(node_attrs.keys()):
            del node_attrs[k]

        graph.add_node(name, self.name, type=Node.LEAF)
        check_nodes.append((self.name, name))
        
        neighbors = graph.neighbors(name, self.name)
        for n, _ in neighbors:
            contexted_name = graph.node_context_name(n)            
            graph.remove_edge(name, self.name, contexted_name[::-1])

            if contexted_name[0] == self.name:
                check_nodes.append(contexted_name)
    
        for context, node_name in check_nodes:
            if graph.in_degree(node_name, context) < 2 and graph[n]['type'] is Node.LEAF:
                graph.remove_node(node_name, contexted_name)
