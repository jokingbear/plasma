import networkx as nx

from ....functional.decorators import propagate


class Graph:

    def __init__(self):
        self._structures = nx.DiGraph()

    def predecessors(self, obj):
        for n in self._structures.predecessors(id(obj)):
            yield self._structures.nodes[n]['object']
    
    def successors(self, obj):
        for n in self._structures.successors(id(obj)):
            yield self._structures.nodes[n]['object']

    @propagate(None)
    def add_queue(self, queue):
        self._structures.add_node(id(queue), object=queue)
    
    @propagate(None)
    def add_block(self, block, distributor=None):
        self._structures.add_node(id(block), object=block)

        if distributor is not None:
            self._structures.add_node(id(block), distributor=distributor)
