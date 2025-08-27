from .contexts import Context
from .managers import Manager
from typing import Hashable


class ManagedContext(Context):
    
    @property
    def manager(self):
        return ContextManager(self.graph)


class ContextManager(Manager):
    
    def context(self, context:Hashable):
        return ManagedContext(self.graph, context)
