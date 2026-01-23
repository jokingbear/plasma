import networkx as nx

from ..object_inquirer import ObjectInquirer, EmptyResult


class Meta:
    
    def __init__(self, graph:nx.Graph, *index_names:str):
        assert 'type' not in index_names
        
        self.graph = graph
        self._indices:dict[str, dict[object, set]] = {a: [] for a in index_names}
        self._type_index:dict[object, set] = []
        self._successors:dict[tuple, dict[object, set]] = {}
        self._predecessors:dict[tuple, dict[object, set]] = {}
    
    def add(self, node_id, type):
        self._indices[type].add(node_id)
        
        data = self.graph.nodes[node_id]['data']
        inquirer = ObjectInquirer()
        for idx_name, value2nodes in self._indices.items():
            result = inquirer.query(data, idx_name)
            if result is not EmptyResult:
                node_set = value2nodes.get(result, set())
                node_set.add(node_id)
                value2nodes[result] = node_set
    
    def get_node_id(self, index_value:object, index_name:str=None):
        if index_name is None:
            return self._type_index.get(index_value, set())
        else:
            return self._indices[index_name].get(index_value, set())

    def __contains__(self, index_name:str):
        return index_name in self._indices
