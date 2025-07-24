from .compute_graph import Graph
from ...functional import State
from ..queues import Queue


class AsyncFlow(Graph, State):
    
    def __init__(self):
        super().__init__()
    
    def run(self):
        return super().run(*inputs, **kwargs)
    
    def put(self, x):
        self.input.put(x)
