import networkx as nx
import inspect

from typing import Hashable
from pathlib import Path
from warnings import warn
from .types import Node
from .links import Link


class Context:
    
    def __init__(self, /, graph:nx.MultiDiGraph=None, name:Hashable=None):        
        if name is None:
            caller = inspect.stack()[1][0]
            caller = inspect.getmodule(caller)
            path = Path(caller.__file__)
            parent_path = path.parent
            name = parent_path.name
        
        graph = graph or nx.MultiDiGraph()
        if name in graph:
            warn(f'context {name} already exists, reusing it!')
        else:
            graph.add_node(name, type=Node.CONTEXT)

        self.context = name
        self.graph = graph
            
    def add_dependency(self, name, value, as_singleton=False):
        assert as_singleton or callable(value), 'dependency should be callable'
        
        if (self.context, name) in self.graph:
            warn(f'{name} is already registered for context {self.context}, overwriting it.')
            neighbors = [*self.graph.neighbors(name)]
            self.graph.remove_edges_from([(name, n) for n in neighbors])
        
        if as_singleton:
            self.graph.add_node(name, type=Node.SINGLETON, value=value)    
        else:
            self.graph.add_node(name, type=Node.INITATOR, value=value)
            
            parameters = inspect.signature(value).parameters
            for arg_name, p in parameters.items():
                if arg_name != 'self':
                    attrs = {}
                    if p.annotation is not inspect._empty:
                        attrs['annotation'] = p.annotation

                    self.graph.add_node(arg_name, **attrs)
                    self.graph.add_edge(name, arg_name, Link.DEPEND_ON)
                    
                    if p.default is not inspect.Parameter.empty:
                        self.graph.add_node(arg_name, type=Node.SINGLETON, value=p.default)

        return self

    def duplicate(self, current_name:str, new_name:str):
        current_name = self.context, current_name
        new_name = self.context, new_name
        
        assert current_name in self.graph, 'current name must be in dep graph'
        assert new_name not in self.graph, 'new name must not be in dep graph'
        
        current_graph = self.graph        
        node_attr = current_graph.nodes[current_name]
        neighbors = [*current_graph.successors(current_name)]
        current_graph.add_node(new_name, **node_attr)
        for n in neighbors:
            current_graph.add_edge(new_name, n)
        
        return self
