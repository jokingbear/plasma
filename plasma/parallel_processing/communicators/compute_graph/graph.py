import networkx as nx

from ....functional import decorators
from ...queues import Queue
from ..distributors import Distributor


class Graph:

    def __init__(self):
        self._structures = nx.DiGraph()

    def chain(self, *chains:tuple[object, Queue, object, Distributor]):
        for head, connector, tail, distributor in chains:            
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
            
        self._merge_queue()
        try:
            self._validate()
        except AssertionError as e:
            raise SyntaxError() from e

        return self

    @decorators.propagate(None)
    def _add_queue(self, queue):
        self._structures.add_node(id(queue), object=queue)
    
    @decorators.propagate(None)
    def _add_block(self, block, distributor=None):
        self._structures.add_node(id(block), object=block)

        if distributor is not None:
            self._structures.add_node(id(block), distributor=distributor)

    def _merge_queue(self):
        mappings = {}
        for n, obj in self._structures.nodes(data='object'):
            if not isinstance(obj, Queue):
                qids = [*self._structures.predecessors(n)]
                if len(qids) > 0:
                    mappings.update({qid: qids[-1] for qid in qids[:-1]})

        if len(mappings) > 0:
            self._structures = nx.relabel_nodes(self._structures, mappings)

    def _validate(self):
        for obj_id, obj in self._structures.nodes(data='object'):
            if isinstance(obj, Queue):
                assert self._structures.out_degree(obj_id) < 2, \
                    f'Queue can only connect to one block - qid={obj_id}'
                
                for block in self._structures.successors(obj_id):
                    assert not isinstance(block, Queue), \
                        f'cannot connect 2 queue - qid={obj_id}'
