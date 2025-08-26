from .contexts import Context
from .managers import Manager
from typing import Hashable


class ManagedContext(Context):
    
    @property
    def manager(self):
        return ContextManager(self._graph)


class ContextManager(Manager):
    
    def init_context(self, context:Hashable):
        return ManagedContext(self._graph, context)
