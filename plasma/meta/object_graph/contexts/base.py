import networkx as nx
import inspect

from typing import Hashable
from pathlib import Path
from warnings import warn
from ..types import Node
from ..context_graph import ContextGraph
from ..links import Link


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
        node_id = self.name, name
        if node_id in graph and graph.type(*node_id) is not Node.LEAF:
            warn(f'{name} is already registered for context {self.name}, overwriting it.')
            self.remove_dependency(name)

        if as_singleton:
            graph.add_node(*node_id, type=Node.SINGLETON, value=value)
        else:
            graph.add_node(*node_id, type=Node.INITATOR, value=value)
            
            parameters = inspect.signature(value).parameters
            for arg_name, p in parameters.items():
                if arg_name != 'self':
                    arg_id = self.name, arg_name
                    attrs = {}
                    if p.annotation is not inspect._empty:
                        attrs['annotation'] = p.annotation
                    
                    if arg_id not in self.graph:
                        attrs['type'] = Node.LEAF
                    
                    if p.default is not inspect.Parameter.empty:
                        attrs['value'] = p.default

                    graph.add_node(*arg_id, **attrs)
                    graph.add_edge(node_id, arg_id)

        return self

    def duplicate(self, current_name:Hashable, new_name:Hashable): 
        graph = self.graph
        current_id = self.name, current_name
        new_id = self.name, new_name
               
        assert current_id in graph, 'current name must be in dep graph'
        assert new_id not in graph, 'new name must not be in dep graph'

        node_attrs = graph[*current_id]
        graph.add_node(*new_id, **node_attrs)
        
        neighbors = graph.successors(*new_id, link=Link.DEPEND_ON)
        for n in neighbors:
            context, _ = n
            if context == self.name:
                self.graph.add_edge(new_id, n)
        
        return self

    def remove_dependency(self, name:Hashable):
        graph = self.graph
        node_id = self.name, name
        
        node_attrs = graph[*node_id]
        for k in list(node_attrs.keys()):
            del node_attrs[k]

        graph.add_node(*node_id, type=Node.LEAF)
        check_nodes = [node_id]
        
        neighbors = [*graph.successors(*node_id, link=Link.DEPEND_ON|Link.DELEGATE_TO)]
        for n, _ in neighbors:     
            graph.remove_edge(node_id, n)
            
            context, _ = n
            if context == self.name:
                check_nodes.append(n)
    
        for n in check_nodes:
            if graph.type(*n) is Node.LEAF:
                graph.remove_node(*n)
