import networkx as nx

from typing import Hashable
from warnings import warn
from .links import Link
from .context.context import Context


class ContextGraph:
    
    def __init__(self, graph:nx.MultiDiGraph=None):
        self._graph = graph
    
    def add(self, context:Context):
        pass
    
    def merge(self, other, **collision_maps:Hashable):
        assert isinstance(other, ContextGraph)
        
        current_graph = self._graph.copy()
        other_graph = other._graph.copy()
        
        current_contexts = self.contexts
        other_contexts = other.contexts
        collisions = current_contexts.intersection(other_contexts)
        if len(collisions) > 0:
            warn(f'context collisions: {collisions}', stacklevel=2)
        
        rename_maps = {c: collision_maps[c] for c in collisions if c in collision_maps}
        drop_maps = collisions.difference(rename_maps)
        
        if len(rename_maps) > 0:
            other_graph = nx.relabel_nodes(other_graph, rename_maps)
        
        if len(drop_maps) > 0:
            for m in drop_maps:
                nodes = [n for _, n, t in current_graph.edges(m) if t is Link.CONTAIN]
                current_graph.remove_nodes_from([m, *nodes])
        
        merged_graph = nx.compose(current_graph, other_graph )
        return type(self)(merged_graph)
    
    def link(self, *links:tuple[str, str]):
        for namespace_head, namespace_tail in links:
            nh, h = namespace_head
            nt, t = namespace_tail
            
            assert (nh, h) in self._graph, f'graph must contain context {nh} with node {h}'
            assert (nt, t) in self._graph, f'graph must contain context {nt} with node {t}'
            
            self._graph.add_edge(namespace_head, namespace_tail, Link.DEPEND_ON)
            
        return self
          
    @property
    def contexts(self):
        contexts = {n[0] for n in self._graph}
        return contexts
