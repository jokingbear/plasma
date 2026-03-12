import networkx as nx

from typing import Callable

from ..schemas import Representation


class StructInitGraph(nx.DiGraph):
    
    def __init__(self, 
                 rep:Representation, 
                 struct:dict,
                 real_to_rep:Callable[[tuple], tuple]):
        super().__init__()
        
        self.__update(rep, real_to_rep, struct, '')
        
    def __update(self, rep:Representation, real_to_rep:Callable[[tuple], tuple], 
                 struct, accessor:tuple):
        rep_accessor = real_to_rep(accessor)
        if rep_accessor not in rep:
            return

        if rep.out_degree(rep_accessor) == 0:
            self.add_node(accessor, value=struct)
        elif isinstance(struct, dict) and len(struct) > 0:
            for k, v in struct.items():
                new_accessor = (*accessor, k)
                self.add_edge(accessor, new_accessor)
                self.__update(rep, real_to_rep, v, new_accessor)
        elif isinstance(struct, list) and len(struct) > 0:
            for i, v in enumerate(struct):
                new_accessor = (*accessor, i)
                self.add_edge(accessor, new_accessor)
                self.__update(rep, real_to_rep, v, new_accessor)
        else:
            self.add_node(accessor, value=struct)
