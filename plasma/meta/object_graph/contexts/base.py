import networkx as nx
import inspect

from typing import Hashable
from pathlib import Path
from warnings import warn
from ..types import Node
from ..links import Link
from .primitive import Primitive


class Base(Primitive):
    
    def __init__(self, graph:nx.MultiDiGraph=None, name:Hashable=None):
        if name is None:
            caller = inspect.stack()[1][0]
            caller = inspect.getmodule(caller)
            path = Path(caller.__file__)
            parent_path = path.parent
            name = parent_path.name

        super().__init__(graph, name)
            
    def add_dependency(self, name:Hashable, value, as_singleton=False):
        assert as_singleton or callable(value), 'dependency should be callable'
        
        if name in self:
            warn(f'{name} is already registered for context {self.name}, overwriting it.')
            self.remove_dependency(name)

        if as_singleton:
            self._add_node(name, type=Node.SINGLETON, value=value)
        else:
            self._add_node(name, type=Node.INITATOR, value=value)
            
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

                    self._add_node(arg_name, **attrs)
                    self._add_edge(name, arg_name)

        return self

    def duplicate(self, current_name:Hashable, new_name:Hashable):        
        assert current_name in self, 'current name must be in dep graph'
        assert new_name not in self, 'new name must not be in dep graph'
               
        node_attrs = self[current_name]
        neighbors = self.neighbors(current_name)
        self._add_node(new_name, **node_attrs)
        for n in neighbors:
            self._add_edge(new_name, n)
        
        return self

    def remove_dependency(self, name:Hashable):
        check_nodes = []
        node_attrs = self[name]
        for k in list(node_attrs.keys()):
            del node_attrs[k]

        self._add_node(name, type=Node.LEAF)
        check_nodes.append(name)
        
        neighbors = self.neighbors(name)
        for n in neighbors:
            self._remove_edge(name, n)
            check_nodes.append(n)
    
        for n in check_nodes:
            if self.in_degree(n) < 2 and self[n]['type'] is Node.LEAF:
                self._remove_node(n)
