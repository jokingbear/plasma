import networkx as nx

from .index import Index
from ..object_inquirer import ObjectInquirer


class Inquirer:
    
    def __init__(self, 
                graph:nx.DiGraph, 
                index:Index
            ):
        
        self.graph = graph
        self._index = index
    
    def nodes(self, node_type, *attrs:str, **other_index_values):
        index_inquirer = self._index.inquirer
        nodes = index_inquirer.nodes(node_type)
        for index_name, index_value in other_index_values.items():
            related_nodes = index_inquirer.nodes(index_value, index_name)
            anchor, reference = sorted([nodes, related_nodes], key=len)
            nodes = anchor.intersection(reference)

        for n in nodes:
            data = self._index.data(n)
            yield select(n, data, ObjectInquirer(), attrs)
    
    def successors(self, node_id, *attrs:str, succ_type=None):
        successors = self._index.inquirer.successors(node_id, succ_type)
        for s in successors:
            data = self._index.data(s)
            yield select(s, data, ObjectInquirer(), attrs)
    
    def predecessors(self, node_id, *attrs:str, pred_type=None):
        predecessors = self._index.inquirer.predecessors(node_id, pred_type)
        for p in predecessors:
            data = self._index.data(p)
            yield select(p, data, ObjectInquirer(), attrs)

    def select(self, node_id, *attrs:str):
        data = self._index.data(node_id)
        assert len(attrs) > 0
        results = select(node_id, data, ObjectInquirer(), attrs)
        return results[1:]

    def type(self, node_id):
        return self._index.type(node_id)
    
    def data(self, node_id):
        return self._index.data(node_id)
    

def select(node_id, data, attr_inquirer:ObjectInquirer, attrs:tuple[str]):
    if len(attrs) == 0:
        return node_id
    else:
        selected_data = (attr_inquirer.get(data, a) for a in attrs)
        return node_id, *selected_data
