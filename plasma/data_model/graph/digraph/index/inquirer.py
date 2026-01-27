import networkx as nx

from typing import Callable, Mapping


class Inquirer:
    
    def __init__(self, 
                graph:nx.DiGraph,
                indices:Mapping[str, Mapping[object, set]],
                successor_indices:Mapping[tuple, Mapping[object, set]],
                predecessor_indices:Mapping[tuple, Mapping[object, set]],
                type_getter:Callable[[object], object]
            ):
        self._graph = graph
        self._indices = indices
        self._type_getter = type_getter
        self._successor_indices = successor_indices
        self._predcessor_indices = predecessor_indices
    
    def nodes(self, index_value, index_name:str=None):
        if index_name is None:
            return self._indices['type'].get(index_value, set())
        elif index_name in self._indices:
            return self._indices[index_name].get(index_value, set())
        
        return set()
    
    def successors(self, node_id, succ_type=None):
        ntype = self._type_getter(node_id)
        if succ_type is None:
            return self._graph.successors(node_id)
        elif (ntype, succ_type) in self._successor_indices:
            return self._successor_indices[ntype, succ_type].get(node_id, set())
        
        return set()
            
    def predecessors(self, node_id, pred_type=None):
        ntype = self._type_getter(node_id)
        if pred_type is None:
            return self._graph.predecessors(node_id)
        elif (ntype, pred_type) in self._predcessor_indices:
            return self._predcessor_indices[ntype, pred_type].get(node_id, set())
        
        return set()
