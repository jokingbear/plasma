import networkx as nx

from warnings import warn
from ..links import Link
from ..types import Node
from ..context_graph import ContextGraph
from ..contexts import Context


class Base:
    
    def __init__(self, graph:ContextGraph=None):
        graph = graph if graph is not None else ContextGraph()
        self.graph = graph

    def merge(self, other):
        assert isinstance(other, (Base))
        
        current_graph = self.graph.copy()
        other_graph = other.graph.copy()
        
        current_contexts = self.contexts
        other_contexts = other.contexts
        collisions = current_contexts.intersection(other_contexts)
        if len(collisions) > 0:
            warn(f'context collisions: {collisions}', stacklevel=2)
        
            for c in collisions:
                current_graph.remove_context(c)
        
        merged_graph = current_graph.merge(other_graph)
        return type(self)(merged_graph)
    
    def link(self, *links:tuple[str, str], inplace=False):
        self = self if inplace else type(self)(self.graph.copy())
        
        for context_head, context_tail in links:
            head = tuple(context_head.split('.'))
            tail = tuple(context_tail.split('.'))
            
            assert head[0] != tail[0], f'{head[0]} is the same as {tail[0]}'
            assert head in self.graph, f'manager does not contain {head[1]} in context {head[0]}'
            assert tail in self.graph, f'manager does not contain {tail[1]} in context {tail[0]}'
                     
            if self.graph.out_degree(*head, link=None) > 0:
                warn(f'{head[0]}.{head[1]} contains dependency, removing it')
                Context(self.graph, head[0]).remove_dependency(head[1])
            
            self.graph.add_edge(head, tail, Link.DELEGATE_TO)
            self.graph.add_node(*head, type=Node.INITATOR)
            
        return self
          
    @property
    def contexts(self):
        return set(self.graph.contexts)
