import networkx as nx

from .nodes import Nodes
from ..index import Index
from ...object_inquirer import ObjectInquirer


class Inquirer[T:nx.DiGraph]:
    
    def __init__(self, graph:T, index:Index):
        
        self.graph = graph
        self._index = index
    
    def nodes(self, node_type:object|list=None, **index_map:object|list):
        assert node_type is not None or len(index_map) > 0, 'must at least use one index'
        
        index_map[self._index.type_index_name] = node_type 
        nodes = self._index.inquirer.nodes(index_map)
        return Nodes(self._index, self, nodes)
    
    def successors(self, node_id, succ_type:object|list=None):
        successors = self._index.inquirer.successors(node_id, succ_type)
        return Nodes(self._index, self, successors)
    
    def predecessors(self, node_id, pred_type:object|list=None):
        predecessors = self._index.inquirer.predecessors(node_id, pred_type)
        return Nodes(self._index, self, predecessors)

    def node_ids(self, node_ids):
        return Nodes(self._index, self, node_ids)
    
    def select(self, node_id, *attrs:str, default=None):
        assert len(attrs) > 0
        data = self.data(node_id)
        inq = ObjectInquirer(data)
        return tuple(inq.get(a, default) for a in attrs)

    def type(self, node_id):
        return self._index.type(node_id)
    
    def data(self, node_id):
        return self._index.data(node_id)
