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
        index = None
        if index_name is None:
            index = self._indices['type']
        elif index_name in self._indices:
            index = self._indices[index_name]
        
        results = None
        if index is not None:
            index_values = index_value
            if not isinstance(index_value, list):
                index_values = [index_value]
            
            results = set()
            for v in index_values:
                results.update(index.get(v, []))
                
        return results or set()
    
    def successors(self, node_id, succ_type=None):
        ntype = self._type_getter(node_id)
        if succ_type is None:
            return self._graph.successors(node_id)
        else:
            succ_types = succ_type
            if not isinstance(succ_type, list):
                succ_types = [succ_type]
            
            for t in succ_types:
                for n in self._successor_indices.get((ntype, t), []):
                    yield n
            
    def predecessors(self, node_id, pred_type=None):
        ntype = self._type_getter(node_id)
        if pred_type is None:
            return self._graph.predecessors(node_id)
        else:
            pred_types = pred_type
            if not isinstance(pred_type, list):
                pred_types = [pred_type]
            
            for t in pred_types:
                for n in self._successor_indices.get((ntype, t), []):
                    yield n
