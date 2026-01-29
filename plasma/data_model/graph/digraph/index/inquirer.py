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
    
    def nodes(self, index_values, index_name:str=None):
        standardized_values = standardize_value(index_values)
        index_name = index_name or 'type'
        index = self._indices['type']        
        results = set()
        for v in standardized_values:
            results.update(index.get(v, []))

        return results
    
    def successors(self, node_id, succ_types:object|list=None):
        ntype = self._type_getter(node_id)
        standardized_types = standardize_value(succ_types)
        if len(standardized_types) == 0:
            for n in self._graph.successors(node_id):
                yield n
        else:            
            for t in standardized_types:
                for n in self._successor_indices.get((ntype, t), {}).get(node_id, []):
                    yield n
            
    def predecessors(self, node_id, pred_types:object|list=None):
        ntype = self._type_getter(node_id)
        standardized_types= standardize_value(pred_types)
        if len(standardized_types) == 0:
            for n in self._graph.predecessors(node_id):
                yield n
        else:
            for t in standardized_types:
                for n in self._predcessor_indices.get((ntype, t), {}).get(node_id, []):
                    yield n

    def rank(self, index_values, index_name:str=None):
        index_values = standardize_value(index_values)
        index_name = index_name or 'type'
        index = self._indices[index_name]
        return sum(len(index.get(v, [])) for v in index_values)


def standardize_value(values:object|list|None):
    if values is None:
        return []
    elif isinstance(values, list):
        return values
    else:
        return [values]
