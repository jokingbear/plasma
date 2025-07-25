import time

from .compute_graph import Graph
from ...functional import State
from ..queues import Queue
from typing import Callable
from ...functional import partials, Identity
from .distributors import Distributor


class AsyncFlow(Graph, State):
    
    def __init__(self):
        super(State, self).__init__()
        super(Graph, self).__init__()

        self._running = False
    
    def run(self):
        for q in self.queues:
            for block_id in self.graph.successors(id(q)):
                block = self.graph.nodes[block_id]['object']
                
                if isinstance(block, Distributor):
                    distributor = block
                    block = Identity()
                else:
                    distributor = self.graph.nodes[block_id]['distributor']

                next_queues:list[Queue] = [self.graph.nodes[next_id]['object'] for next_id in self.graph.successors(block_id)]
                un_named_queues = [nq for nq in next_queues if nq.name is None]
                named_queues = {nq.name: nq for nq in next_queues if nq.name is not None}
                q.register_callback(block)\
                    .chain(partials(distributor, *un_named_queues, **named_queues, pre_apply_before=False))\
                        .run()
        self._running = True
        return self
    
    def put(self, x):
        self.input.put(x)
        
    def release(self):
        for q in self.queues:
            if self.graph.out_degree(id(q)) > 0:
                q.release()

    def on_exception(self, handler:Callable[[int, object, Exception], None]):
        for q in self.queues:
            q.on_exception(partials(handler, id(q)))
    
    @property
    def running(self):
        self._running = self._running

    def __enter__(self):
        return self.run()
    
    def __exit__(self, *args, **kwargs):
        self.release()

    def block(self):
        while True:
            time.sleep(2 * 60 * 60)

    def alive(self):
        return all(q.is_alive() for q in self.queues if self.graph.out_degree(id(q)) > 0)
