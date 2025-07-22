from ...functional import I2O
from typing import Callable
from .manager1 import Manager


class Manager2(Manager):
    
    def add_decorator_provider(self, decorator_provider:I2O[str, Callable, Callable]):
        for n in self._dep_graph:
            if 'initiator' in self._dep_graph.nodes[n]:
                intiator = self._dep_graph.nodes[n]['initiator']
                new_initiator = decorator_provider(n, intiator)
                self._dep_graph.nodes[n]['initiator'] = new_initiator
        
        return self
    
    def add_wrapper(self, wrapper:Callable[[str, object], object]):
        self.injector.update_wrapper(wrapper)
        return self
