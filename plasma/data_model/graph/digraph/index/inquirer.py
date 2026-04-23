import networkx as nx

from typing import Any, Callable, Mapping
from .sub_indexes import NodeSubIndex, EdgeSubindex
from ....collections import ZippedStream


class Inquirer:
    
    def __init__(
            self, 
            graph:nx.DiGraph,
            sub_indices:Mapping[str, NodeSubIndex],
            successor:EdgeSubindex,
            predecessor:EdgeSubindex,
            type_getter:Callable[[object], object]
        ):
        self._graph = graph
        self._indices = sub_indices
        self._type_getter = type_getter
        self._successor_indices = successor
        self._predcessor_indices = predecessor
    
    def nodes(self, **index_queries:Any|list):
        results = (
            ZippedStream(index_queries.items())
            .sort(lambda k,_: len(self._indices[k]))
            .accumulate(
                [], 
                lambda iname, q: self._indices[iname].get(q),
                list.extend
            )
        )

        return set(results)
    
    def successors(self, node_id, succ_types:object|list=None):
        return _neigbors(self._successor_indices, node_id, succ_types)
            
    def predecessors(self, node_id, pred_types:object|list=None):
        return _neigbors(self._predcessor_indices, node_id, pred_types)


def _neigbors(index:EdgeSubindex, node_id, ntypes:Any|list|None=None):
    return set(index.get(node_id, ntypes))
