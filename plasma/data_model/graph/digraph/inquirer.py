import networkx as nx

from .index import Index
from ..object_inquirer import ObjectInquirer
from ....functional import auto_map


class Inquirer:
    
    def __init__(self, 
                graph:nx.DiGraph, 
                index:Index
            ):
        
        self.graph = graph
        self._index = index
    
    def nodes(self, node_type:object|list, *attrs:str, **index_map:object|list):
        index_inquirer = self._index.inquirer
        index_map[None] = node_type
        values_keys = sorted(
                            ((idv, idk) for idk, idv in index_map.items()), 
                            key=auto_map(index_inquirer.rank), reverse=True
                        )
        nodes = index_inquirer.nodes(*values_keys[0])
        for vk in values_keys[1:]:
            nodes.update(index_inquirer.nodes(*vk))

        for n in nodes:
            data = self._index.data(n)
            yield select(n, data, ObjectInquirer(), attrs)
    
    def successors(self, node_id, succ_type:object|list=None, *attrs:str):
        successors = self._index.inquirer.successors(node_id, succ_type)
        for s in successors:
            data = self._index.data(s)
            yield select(s, data, ObjectInquirer(), attrs)
    
    def predecessors(self, node_id, pred_type:object|list=None, *attrs:str):
        predecessors = self._index.inquirer.predecessors(node_id, pred_type)
        for p in predecessors:
            data = self._index.data(p)
            yield select(p, data, ObjectInquirer(), attrs)

    def select(self, node_id, *attrs:str):
        assert len(attrs) > 0
        data = self.data(node_id)
        return ObjectInquirer().select(data, attrs)

    def type(self, node_id):
        return self._index.type(node_id)
    
    def data(self, node_id):
        return self._index.data(node_id)
    

def select(node_id, data, attr_inquirer:ObjectInquirer, attrs:tuple[str]):
    if len(attrs) == 0:
        return node_id
    else:
        return node_id, *attr_inquirer.select(data, attrs)
