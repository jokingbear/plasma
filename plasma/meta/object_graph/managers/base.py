import networkx as nx

from warnings import warn
from ..links import Link
from ..contexts import Context
from ..types import Node
from ..context_graph import ContextGraph


class Base:
    
    def __init__(self, graph:ContextGraph=None):
        graph = graph if graph is not None else ContextGraph()
        self._graph = graph

    def merge(self, other):
        assert isinstance(other, Base)
        
        current_graph = self._graph.copy()
        other_graph = other._graph.copy()
        
        current_contexts = self.contexts
        other_contexts = other.contexts
        collisions = current_contexts.intersection(other_contexts)
        if len(collisions) > 0:
            warn(f'context collisions: {collisions}', stacklevel=2)
        
            for m in collisions:
                nodes = [n for _, n, t in current_graph.edges(m) if t is Link.CONTAINS]
                current_graph.remove_nodes_from([m, *nodes])
        
        merged_graph = nx.compose(current_graph, other_graph )
        return type(self)(merged_graph)
    
    def link(self, *links:tuple[str, str], inplace=False):
        self = self if inplace else type(self)(self._graph.copy())
        
        for context_head, context_tail in links:
            head_namespace, head = context_head.split('.')
            tail_namespace, tail = context_tail.split('.')
            
            assert head_namespace in self._graph, f'manager does not contain {head_namespace}'
            assert tail_namespace in self._graph, f'manager does not contain {tail_namespace}'
            assert head_namespace != tail_namespace, f'{head_namespace} is the same as {tail_namespace}'
            
            head_context = Context(self._graph, head_namespace)
            tail_context = Context(self._graph, tail_namespace)            
            if head_context.out_degree(head) > 0:
                warn(f'{head_namespace}.{head} contains dependency, removing it')
                head_context.remove_dependency(head)
            
            hid = head_context.node_id(head)
            tid = tail_context.node_id(tail)
            self._graph.add_edge(hid, tid, Link.DELEGATE_TO)
            
        return self
          
    @property
    def contexts(self):
        contexts = {n for n, ntype in self._graph.nodes('type') if ntype is Node.CONTEXT}
        return contexts
