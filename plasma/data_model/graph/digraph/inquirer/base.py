import networkx as nx

from ..index import Index
from ...object_inquirer import ObjectInquirer
from .....functional import auto_map
from .nodes import Nodes


class Inquirer:
    
    def __init__(self, 
                graph:nx.DiGraph, 
                index:Index
            ):
        
        self.graph = graph
        self._index = index
    
    def nodes(self, node_type:object|list=None, **index_map:object|list):
        assert node_type is not None or len(index_map) > 0, 'must at least use one index'
        
        index_inquirer = self._index.inquirer
        if node_type is not None:
            index_map[None] = node_type

        values_keys = sorted(
                            ((idv, idk) for idk, idv in index_map.items()), 
                            key=auto_map(index_inquirer.rank)
                        )
        nodes = index_inquirer.nodes(*values_keys[0])
        for vk in values_keys[1:]:
            nodes.intersection_update(index_inquirer.nodes(*vk))

        return Nodes(self._index, nodes)
    
    def successors(self, node_id, succ_type:object|list=None):
        successors = self._index.inquirer.successors(node_id, succ_type)
        return Nodes(self._index, successors)
    
    def predecessors(self, node_id, pred_type:object|list=None):
        predecessors = self._index.inquirer.predecessors(node_id, pred_type)
        return Nodes(self._index, predecessors)

    def select(self, node_id, *attrs:str):
        assert len(attrs) > 0
        data = self.data(node_id)
        return ObjectInquirer(data).select(attrs)

    def type(self, node_id):
        return self._index.type(node_id)
    
    def data(self, node_id):
        return self._index.data(node_id)
    

def select(node_id, data_inquirer:ObjectInquirer, attrs:tuple[str]):
    if len(attrs) == 0:
        return node_id
    else:
        return node_id, *data_inquirer.select(attrs)
