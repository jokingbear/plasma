from .dependency_injector import DependencyInjector
from ..functional import I2O
from typing import Callable


class DependencyManager(DependencyInjector):
    
    def add_decorator_provider(self, decorator_provider:I2O[str, Callable, Callable]):
        for n in self._dep_graph:
            if 'initiator' in self._dep_graph.nodes[n]:
                intiator = self._dep_graph.nodes[n]['initiator']
                new_initiator = decorator_provider(n, intiator)
                self._dep_graph.nodes[n]['initiator'] = new_initiator
        
        return self
