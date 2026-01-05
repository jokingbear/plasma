import networkx as nx

from .meta import Meta
from pathlib import Path
from .types import Node


class Inquirer:
    
    def __init__(self, meta:Meta, context_graph:nx.DiGraph):
        self.graph = context_graph
        self.meta = meta
    
    def find_context(self, file:Path):
        for p in self.meta:
            if file.is_relative_to(p):
                return p

        return None
    
    def select(self, node_id, *attrs, default=None):
        for a in attrs:
            yield self.graph.nodes[node_id].get(a, default)
    
    def type(self, node_id) -> Node:
        return self.graph.nodes[node_id]['type']

    def node_names(self, context):
        for n in self.meta[context]:
            yield n

    def context_in_degree(self, n):
        in_context_predecessors = [m for m in self.graph.predecessors(n) if m[0] == n[0]]
        return len(in_context_predecessors)
    
    def context_out_degree(self, n):
        in_context_successors = [m for m in self.graph.successors(n) if m[0] == n[0]]
        return len(in_context_successors)
