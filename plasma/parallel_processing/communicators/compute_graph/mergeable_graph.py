import networkx as nx

from .readable_graph import ReadableGraph


class MergeableGraph(ReadableGraph):
    
    def merge(self, other_graph:ReadableGraph):
        self._structures = nx.compose(self._structures, other_graph._structures)
        return self
