from typing import Callable
from .dependency_manager import Manager
from .decorable_injector import DependencyInjector
from warnings import deprecated


class Manager2(Manager):
    
    @deprecated('this method is deprecated, please use add_wrapper instead')
    def add_decorator_provider(self, decorator_provider:Callable[[str, type], type]):
        for n in self._dep_graph:
            if 'initiator' in self._dep_graph.nodes[n]:
                intiator = self._dep_graph.nodes[n]['initiator']
                new_initiator = decorator_provider(n, intiator)
                self._dep_graph.nodes[n]['initiator'] = new_initiator
        
        return self
    
    def add_wrapper(self, wrapper:Callable[[str, object], object]):
        self.injector = DependencyInjector(wrapper)
        return self

    @property
    def entries(self):
        leaves = {}
        for n, val in self._dep_graph.nodes(data='value', default=NotInitalized):
            if self._dep_graph.out_degree(n) == 0:
                leaves[n] = val
        
        return leaves


class NotInitalized:
    pass
