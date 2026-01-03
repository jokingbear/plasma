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
    
    def select(self, node_id, *attrs):
        for a in attrs:
            yield self.graph.nodes[node_id][a]
    
    def type(self, node_id) -> Node:
        return self.graph.nodes[node_id]['type']
