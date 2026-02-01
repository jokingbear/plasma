import networkx as nx

from collections import defaultdict
from .node_editor import NodeEditor
from .edge_editor import EdgeEditor
from .inquirer import Inquirer
from ...object_inquirer import ObjectInquirer


class Index:
    
    def __init__(self, graph:nx.DiGraph, index_names:tuple[str]):
        assert 'type' not in index_names
        
        self.graph = graph
        indices = {n: defaultdict(lambda: set()) for n in index_names}
        indices['type'] = defaultdict(lambda: set())    
        self._indices = indices
        self._successors = defaultdict(lambda: defaultdict(lambda: set()))
        self._predecessors = defaultdict(lambda: defaultdict(lambda: set()))
    
    @property
    def node_editor(self):
        return NodeEditor(self.graph, self._indices, 
                          self._get_index_values, 
                          self.edge_editor
                        )
    
    @property
    def edge_editor(self):
        return EdgeEditor(self._successors, self._predecessors, self.type)
    
    @property
    def inquirer(self):
        return Inquirer(self.graph, self._indices, 
                        self._successors, self._predecessors,
                        self.type
                    )

    def _get_index_values(self, node_id):
        results = {'type': self.type(node_id)}
        inquirer = ObjectInquirer(self.data(node_id))   
        for k in self._indices:
            if k != 'type':
                index_value = inquirer.get(k)
                if index_value is not None:
                    results[k] = index_value

        return results

    def type(self, node_id):
        return self.graph.nodes[node_id]['type']

    def data(self, node_id):
        return self.graph.nodes[node_id]['data']

    @property
    def names(self):
        return [k for k in self._indices if k != 'type']
