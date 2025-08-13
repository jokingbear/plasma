import inspect
import networkx as nx
import re
import typing

from ...functional import AutoPipe
from .decorable_injector import DependencyInjector


class Manager(AutoPipe):

    def __init__(self):
        super().__init__()
        
        self._dep_graph = nx.DiGraph()
        self.injector = DependencyInjector()

    def run(self, *names:str, **init_args) -> dict:
        results = self.injector.run(self._dep_graph, *names, **init_args)
        return results
    
    def add_dependency(self, name, value, as_singleton=False):
        assert as_singleton or callable(value), 'depdency should be callable'
        
        if name in self._dep_graph:
            neighbors = [*self._dep_graph.neighbors(name)]
            self._dep_graph.remove_edges_from([(name, n) for n in neighbors])
        
        if as_singleton:
            self._dep_graph.add_node(name, value=value)    
        else:
            self._dep_graph.add_node(name, initiator=value)
            
            parameters = inspect.signature(value).parameters
            for arg_name, p in parameters.items():
                if arg_name != 'self':
                    attrs = {}
                    if p.annotation is not inspect._empty:
                        attrs['annotation'] = p.annotation

                    self._dep_graph.add_node(arg_name, **attrs)
                    self._dep_graph.add_edge(name, arg_name)
                    
                    if p.default is not inspect.Parameter.empty:
                        self._dep_graph.add_node(arg_name, value=p.default)

        return self

    def merge(self, manager):
        assert isinstance(manager, Manager), 'manager must be meta.object_graph.Manager instance'
        self._dep_graph = nx.compose(self._dep_graph, manager._dep_graph)

        return self

    def duplicate(self, current_name:str, new_name:str):
        assert current_name in self._dep_graph, 'current name must be in dep graph'
        assert new_name not in self._dep_graph, 'new name must not be in dep graph'
        
        node = self._dep_graph.nodes[current_name]
        neighbors = [*self._dep_graph.successors(current_name)]
        self._dep_graph.add_node(new_name, **node)
        for n in neighbors:
            self._dep_graph.add_edge(new_name, n)
        
        return self
