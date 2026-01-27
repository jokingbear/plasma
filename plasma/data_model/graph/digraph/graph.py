import networkx as nx
import itertools

from .index import Index
from .inquirer import Inquirer


class DiGraph(nx.DiGraph):
    
    def __init__(self, *index_names:str):
        super().__init__()
        
        self._index = Index(self, index_names)

    @property
    def inquirer(self):
        return Inquirer(self, self._index)
    
    def add_node(self, node_for_adding, type, data=None):
        super().add_node(node_for_adding, type=type, data=data)
        
        self._index.node_editor.add(node_for_adding)
    
    def add_nodes_from(self, nodes_for_adding):
        iter1, iter2 = itertools.tee(nodes_for_adding)
        valid_nodes = []
        for n, *attrs in iter1:
            assert len(attrs) == 1
            assert 'type' in attrs
            assert 'data' in attrs
            if n in self:
                self._index.node_editor.delete(n)
            valid_nodes.append(n)
            
        super().add_nodes_from(iter2)
        
        node_editor = self._index.node_editor
        for n in valid_nodes:
            node_editor.add(n)
    
    def add_edge(self, u_of_edge, v_of_edge, **attr):
        super().add_edge(u_of_edge, v_of_edge, **attr)
        self._index.edge_editor.add(u_of_edge, v_of_edge)
    
    def add_edges_from(self, ebunch_to_add, **attr):
        iter1, iter2 = itertools.tee(ebunch_to_add)
        super().add_edges_from(iter1, **attr)
        
        edge_editor = self._index.edge_editor
        for n1, n2, *_ in iter2:
            edge_editor.add(n1, n2)

    def remove_edge(self, u, v):
        super().remove_edge(u, v)
        self._index.edge_editor.delete(u, v)
    
    def remove_edges_from(self, ebunch):
        iter1, iter2 = itertools.tee(ebunch)
        super().remove_edges_from(iter1)
        
        edge_editor = self._index.edge_editor
        for n1, n2, *_ in iter2:
            edge_editor.delete(n1, n2)
