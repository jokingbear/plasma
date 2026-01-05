from .context_graph import ContextGraph, Node
from typing import Callable
from inspect import FrameInfo, signature
from pathlib import Path
from warnings import warn


class Registrator:
    
    def __init__(self, graph:ContextGraph, context:str, name:str, source:str):
        self.graph = graph
        
        inquirer = self.graph.inquirer
        node_id = context, name
        if node_id in self.graph and inquirer.type(node_id) is not Node.LEAF:
            file, = inquirer.select(node_id, 'source')
            warn(f'{name} is already registered in {context} in {file}, overriding with {source}')
            
        self.node_id = node_id
        self.source = source

    def register_type(self, cls:type|Callable):
        self.graph.add_node(self.node_id, type=Node.INITIATOR, value=cls, source=self.source)
        
        for param_info in signature(cls).parameters.values():
            child_id = self.node_id[0], param_info.name
            if child_id not in self.graph:
                node_type, value = (Node.LEAF, param_info.annotation) if param_info.default is param_info.empty \
                                    else (Node.SINGLETON, param_info.default)

                self.graph.add_node(child_id, type=node_type, value=value, source=self.source)
            self.graph.add_edge(self.node_id, child_id)
    
    def register_singleton(self, obj):
        self.graph.add_node(self.node_id, type=Node.SINGLETON, value=obj, source=self.source)

    def _trace_context(self, caller_frame:FrameInfo):
        file = Path(caller_frame.filename)
        context = self.graph.inquirer.find_context(file)
        
        if context is None:
            raise ReferenceError(f'{file} has no context initiated, use init_context')
        
        return context, file
