import networkx as nx
import typing
import re

from .manager2 import Manager2
from .helpers import render_annotation


class FactoryManager(Manager2):
    
    def init_factory(self, name:str):
        factory = DependencyFactory(name, self)
        self._dep_graph.add_node(name, factory=factory)
        return factory
    
    def _link_factory(self, factory_name:str, *names:str):
        for n in names:
            self._dep_graph.add_edge(factory_name, n)
        
        return self


class DependencyFactory:
    
    def __init__(self, factory_name:str, manager:FactoryManager):
        self.name = factory_name
        self._dep_manager = manager
        self._registered_names = []
    
    def register(self, *names):  
        self._registered_names.extend(names)
              
        def decorate(cls):
            for n in names:
                self._dep_manager.add_dependency(n, cls)\
                    ._link_factory(self.name, *names)
                
            return cls
        
        return decorate
    
    def register_singleton(self, name, obj):
        self._registered_names.append(name)
        self._dep_manager.add_dependency(name, obj, as_singleton=True)
        self._dep_manager._link_factory(self.name, name)
        
    def __repr__(self):
        return (
            f'{type(self).__name__}(\n'
            f'\tname={self.name},\n'
            f'\tegistered_names={self._registered_names}\n'
            ')'
        )

