import inspect

from inspect import FrameInfo
from ...utils import get_caller_frame
from .state import CONTEXT_GRAPH
from .context_graph import Node
from .registrator import Registrator


class Factory:
    
    def __init__(self, name:str):
        caller = get_caller_frame()
        self.graph = CONTEXT_GRAPH
        context, source = self._trace_context(caller)
        self.graph.add_node((context, name), type=Node.FACTORY, source=source)
        
        self.context = context
        self.name = name
    
    def register(self, *names):
        assert len(names) > 0
        
        caller = get_caller_frame()
        registrators = [Registrator(self.graph, self.context, n,  caller.filename) for n in names]
        def decorator(cls):
            for r in registrators:
                r.register_type(cls)
                self.graph.add_edge((self.context, self.name), r.node_id)
            
            return cls
        
        return decorator
    
    def __setitem__(self, key, value):
        caller = get_caller_frame()
        context, file = self._trace_context(caller)
        
        registrator = Registrator(self.graph, context, key, file)
        registrator.register_singleton(value)
        self.graph.add_edge((self.context, self.name), registrator.node_id)
    
    def _trace_context(self, caller_info:FrameInfo):
        file = caller_info.filename
        package = inspect.getmodule(caller_info.frame).__package__
        context = self.graph.inquirer.find_context(package)
        
        if context is None:
            raise ReferenceError(f'{file} has no context initiated, use init_context')
        
        return context, file
