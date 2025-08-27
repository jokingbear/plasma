import inspect

from .contexts import Context
from .managers import Manager
from typing import Hashable
from pathlib import Path


class ManagedContext(Context):
    
    @property
    def manager(self):
        return ContextManager(self.graph)


class ContextManager(Manager):
    
    def context(self, context:Hashable=None):
        if context is None:
            caller = inspect.stack()[1][0]
            caller = inspect.getmodule(caller)
            path = Path(caller.__file__)
            parent_path = path.parent
            context = parent_path.name
        
        return ManagedContext(self.graph, context)
