import networkx as nx

from warnings import warn
from ..links import Link
from ..contexts import Context
from ..types import Node


class Manager:
    
    def __init__(self, graph:nx.MultiDiGraph=None):
        graph = graph if graph is not None else nx.MultiDiGraph()
        self._graph = graph

    def merge(self, other):
        assert isinstance(other, Manager)
        
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
    
    def link(self, *links:tuple[str, str]):
        for namespace_head, namespace_tail in links:
            nh, h = namespace_head.split('.')
            nt, t = namespace_tail.split('.')
            
            assert (nh, h) in self._graph, f'graph must contain context {nh} with node {h}'
            assert (nt, t) in self._graph, f'graph must contain context {nt} with node {t}'
            
            self._graph.add_edge(namespace_head, namespace_tail, Link.DEPEND_ON)
            
        return self
    
    def init_context(self, context:str):
        return Context(self._graph, context)
          
    @property
    def contexts(self):
        contexts = {n for n, ntype in self._graph.nodes('type') if ntype is Node.CONTEXT}
        return contexts
