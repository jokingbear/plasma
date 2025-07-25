import networkx as nx

from ....functional import decorators
from ...queues import Queue
from ..distributors import Distributor


class Graph:

    def __init__(self):
        self._structures = nx.DiGraph()

    def chain(self, *blocks:tuple[object, Queue, object, Distributor]):
        for head, connector, tail, distributor in blocks:            
            assert not isinstance(head, Queue) \
                    and not isinstance(tail, Queue), f'Queue cannot be used as a block'
            
            self._add_block(head)
            self._add_block(tail, distributor)
            self._add_queue(connector)
            
            if head is None:
                self._structures.add_edge(id(connector), id(tail))
            elif tail is None:
                self._structures.add_edge(id(head), id(connector))
            elif connector is None:
                current_connector = [*self._structures.predecessors(id(tail))]
                assert len(current_connector) == 1
                current_connector = current_connector[0]
                self._structures.add_edge(id(head), current_connector)
            else:
                self._structures.add_edges_from([(id(head), id(connector)), 
                                                 (id(connector), id(tail))])
            
            if connector is not None and tail is not None:
                self._check_consistency(connector, tail)
        
        return self

    @decorators.propagate(None)
    def _add_queue(self, queue):
        self._structures.add_node(id(queue), object=queue)
    
    @decorators.propagate(None)
    def _add_block(self, block, distributor=None):
        self._structures.add_node(id(block), object=block)

        if distributor is not None:
            self._structures.add_node(id(block), distributor=distributor)

    def _check_consistency(self, connector, tail):
        redundant_nodes = []
        for n in self._structures.predecessors(id(tail)):
            if n != id(connector):
                redundant_nodes.append(n)
        
        self._structures.remove_nodes_from(redundant_nodes)
