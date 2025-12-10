from .context_graph import ContextGraph
from .types import Node
from .links import Link
from pathlib import Path
from ..utils import get_caller_frame


class Factory:
    
    def __init__(self, name:str=None, context:str=None, graph:ContextGraph=None):
        name = name or 'factory'
        
        if context is None:
            context = Path(get_caller_frame().filename).parent.name
        
        if graph is None:
            graph = ContextGraph()
            graph.add_context(context)
        
        graph.add_node(context, name, type=Node.FACTORY, value=self)
        self.name = name
        self.context = context
        self.graph = graph
    
    def register(self, *names):  
        assert len(names) > 0, 'must at least have one name'
              
        def decorate(cls):
            for n in names:
                self.graph.add_node(self.context, n, type=Node.INITATOR, value=cls)
                self.graph.add_edge((self.context, self.name), (self.context, n), Link.SUBITEM)
            return cls
        
        return decorate
    
    def register_singleton(self, name, obj):
        self.graph.add_node(self.context, name, type=Node.SINGLETON, value=obj)
        self.graph.add_edge((self.context, self.name), (self.context, name), Link.SUBITEM)
        return self
    
    def __setitem__(self, key, obj):
        self.register_singleton(key, obj)
