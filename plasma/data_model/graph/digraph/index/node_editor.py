import networkx as nx

from typing import Iterable, Protocol
from .sub_indexes import NodeSubIndex


class EdgeEditor(Protocol):
    
    def add(self, node1, node2):...
    
    def delete(self, node1, node2):...


class NodeEditor:
    
    def __init__(
            self,
            graph:nx.DiGraph,
            indices:Iterable[NodeSubIndex],
            edge_editor:EdgeEditor
        ):
        self.graph = graph
        self.indices = indices
        self.edge_editor = edge_editor
    
    def add(self, node_id):
        for i in self.indices:
            i.add(node_id)
        
        for succ in self.graph.successors(node_id):
            self.edge_editor.add(node_id, succ)
        
        for pred in self.graph.predecessors(node_id):
            self.edge_editor.add(pred, node_id)
    
    def delete(self, node_id):
        for i in self.indices:
            i.delete(node_id)
            
        for succ in self.graph.successors(node_id):
            self.edge_editor.delete(node_id, succ)
        
        for pred in self.graph.predecessors(node_id):
            self.edge_editor.delete(pred, node_id)

