import networkx as nx

from ..schemas import Realization


class StructState(dict):
    
    def __init__(self, r:Realization):
        super().__init__()

        temp_graph = nx.DiGraph()
        temp_graph.add_nodes_from(r.nodes)
        temp_graph.add_edges_from(r.edges)
        temp_graph.add_node(r.root, value=self)
        
        for s in r.successors(r.root):
            self.__update(r, temp_graph, s)
        
    def __update(self, r:Realization, values:nx.DiGraph, key):
        predecessor, = values.predecessors(key)
        container = values.nodes[predecessor]['value']
        
        successors = [*values.successors(key)]
        if len(successors) == 0:
            value = r.value(key)
        elif isinstance(successors[0][-1], int):
            value = [{} for _ in successors]
        elif isinstance(key[-1], int):
            value = container[key[-1]]
        else:
            value = {}
            
        container[key[-1]] = value
        values.add_node(key, value=value)
    
        for s in successors:
            self.__update(r, values, s)
