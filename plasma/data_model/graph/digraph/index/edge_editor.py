from networkx import DiGraph

from .sub_indexes import EdgeSubindex


class EdgeEditor:
    
    def __init__(
            self, 
            graph:DiGraph,
            successors:EdgeSubindex,
            predecessors:EdgeSubindex,
        ):
        
        self.graph = graph
        self.successors = successors
        self.predecessors = predecessors
    
    def add(self, node1, node2):
        self.successors.add(node1, node2)
        self.predecessors.add(node2, node1)
    
    def delete(self, node1, node2):
        self.successors.delete(node1, node2)
        self.predecessors.delete(node2, node1)

