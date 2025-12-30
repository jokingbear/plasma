from .context_graph import ContextGraph
from .types import Node
from .links import Link
from pathlib import Path
from ..utils import get_caller_frame
from .contexts.base import Base


class Factory:
    
    def __init__(self, name:str=None, context:Base=None):
        name = name or 'factory'
        
        if context is None:
            context_name = Path(get_caller_frame().filename).parent.name
            context = Base(ContextGraph(), context_name)
        
        self.name = name
        self._context = context
        self.graph.add_node(context.name, name, type=Node.FACTORY, value=self)
    
    def register(self, *names):  
        assert len(names) > 0, 'must at least have one name'
              
        def decorate(cls):
            is_class = isinstance(cls, type)
            for n in names:
                self._context.add_dependency(n, cls, as_singleton=not is_class)
                self.graph.add_edge((self.context, self.name), (self.context, n), Link.SUBITEM)
            return cls
        
        return decorate
    
    def register_singleton(self, name, obj):
        self._context.add_dependency(name, obj, as_singleton=True)
        self.graph.add_edge((self.context, self.name), (self.context, name), Link.SUBITEM)
        return self
    
    def __setitem__(self, key, obj):
        self.register_singleton(key, obj)

    @property
    def context(self):
        return self._context.name

    @property
    def graph(self):
        return self._context.graph

    def update_graph(self, new_graph:ContextGraph):
        self._context = Base(new_graph, self._context.name)
