import networkx as nx

from collections import defaultdict
from typing import Callable


class EdgeEditor:
    
    def add(self, node1, node2):...
    
    def delete(self, node1, node2):...


class NodeEditor:
    
    def __init__(self,
                graph:nx.DiGraph,
                indices:dict[str, defaultdict[object, set]],
                index_getter:Callable[[object], dict],
                edge_editor:EdgeEditor
            ):
        self._graph = graph
        self.indices = indices
        self.index_getter = index_getter
        self.edge_editor = edge_editor
    
    def add(self, node_id):
        index_name_values = self.index_getter(node_id)
        for idxn, idxv in index_name_values.items():
            self.indices[idxn][idxv].add(node_id)
        
        for succ in self._graph.successors(node_id):
            self.edge_editor.add(node_id, succ)
        
        for pred in self._graph.predecessors(node_id):
            self.edge_editor.add(pred, node_id)
    
    def delete(self, node_id):
        index_name_values = self.index_getter(node_id)
        for idxn, idxv in index_name_values.items():
            self.indices[idxn][idxv].remove(node_id)
        
        for succ in self._graph.successors(node_id):
            self.edge_editor.delete(node_id, succ)
        
        for pred in self._graph.predecessors(node_id):
            self.edge_editor.delete(pred, node_id)
