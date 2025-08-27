import inspect

from .contexts import Context
from .managers import Manager
from typing import Hashable
from pathlib import Path


class AutoContext(Context):
    
    def __init__(self, graph=None, name=None):
        if name is None:
            caller = inspect.stack()[1][0]
            caller = inspect.getmodule(caller)
            path = Path(caller.__file__)
            parent_path = path.parent
            name = parent_path.name
        
        graph = graph or ContextManager().graph
        super().__init__(graph, name)
    
    @property
    def context_manager(self):
        return ContextManager(self.graph)
    
    def link(self, other_context, *links:str|tuple[str, str]):
        assert isinstance(other_context, AutoContext)
        
        self_manager = self.context_manager
        other_manager = other_context.context_manager
        assert self_manager == other_manager, 'context needs to be merged first, use merge context manager first'
        
        standardized_links = []
        for ht in links:
            if isinstance(ht, str):
                head = tail = ht
            else:
                head, tail = ht
            
            standardized_links.append((f'{self.name}.{head}', f'{other_context.name}.{tail}'))

        self_manager.link(*standardized_links, inplace=True)
        return self

    def link_name(self, other_context):
        assert isinstance(other_context, AutoContext)
        
        names = {n for (_, n), in self.graph.nodes(self.name)}
        other_names = {n for (_, n), in self.graph.nodes(other_context.name)}
        matched_names = names.intersection(other_names)
        return self.link(other_context, *matched_names)


class ContextManager(Manager):
    
    def context(self, context:Hashable=None):        
        return AutoContext(self.graph, context)

    def __eq__(self, value):
        
        return isinstance(value, ContextManager) and self.graph is value.graph
