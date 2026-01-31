from collections import defaultdict
from typing import Callable


class EdgeEditor:
    
    def __init__(self, 
                successors:defaultdict[tuple, defaultdict[object, set]],
                predecessors:defaultdict[tuple, defaultdict[object, set]],
                edge_types:set[tuple],
                type_getter:Callable[[object], object]
            ):
        
        self.successors = successors
        self.predecessors = predecessors
        self.edge_types = edge_types
        self.type_getter = type_getter
    
    def add(self, node1, node2):
        ntype1 = self.type_getter(node1)
        ntype2 = self.type_getter(node2)
        
        self.successors[ntype1, ntype2][node1].add(node2)
        self.predecessors[ntype2, ntype1][node2].add(node1)
        self.edge_types.add((ntype1, ntype2))
    
    def delete(self, node1, node2):
        ntype1 = self.type_getter(node1)
        ntype2 = self.type_getter(node2)
        
        self.successors[ntype1, ntype2][node1].remove(node2)
        self.predecessors[ntype2, ntype1][node2].remove(node1)
        
        if len(self.successors[ntype1, ntype2]) == 0:
            pass
