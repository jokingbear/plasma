import pandas as pd

from .renderable import RenderableContext
from ....functional import AutoPipe
from ..context_graph import ContextGraph
from ..links import Link
from ..types import Node


class RunnableContext(RenderableContext, AutoPipe):
    
    def __init__(self, graph, name = None):
        AutoPipe.__init__(self)
        RenderableContext.__init__(self, graph, name)

    def run(self, *names, allow_global=True, **kwargs):
        for n in names:
            assert (self.name, n) in self.graph, f'context {self.name} does not contain {n}'
        
        initiator = GraphInitiator(self.graph, self.name, allow_global, kwargs)
        for n in names:
            initiator.run((self.name, n))
        
        return pd.Series(initiator.results)[list(names)]


class NotIntialized: pass


class GraphInitiator(AutoPipe):
    
    def __init__(self, graph:ContextGraph, context, allow_global:bool, inputs:dict[str, object]):
        super().__init__()

        self.graph = graph
        self.context = context
        self.allow_global = allow_global
        
        initiated = {}
        for k, v in inputs.items():
            if k in self.graph and isinstance(v, dict):
                for k1, v1 in v.items():
                    initiated[k, k1] = v1
            else:
                initiated[context, k] = v

        self._initiated = initiated
    
    def run(self, node_id):
        if node_id not in self._initiated:
            if (self.context, node_id[1]) in self._initiated and self.allow_global:
                self._initiated[node_id] = self._initiated[self.context, node_id[1]]
            elif self.graph.type(*node_id) is Node.SINGLETON:
                self._initiated[*node_id] = self.graph.value(*node_id)
            elif self.graph.type(*node_id) is Node.LEAF:
                raise ReferenceError(f'no input for {node_id[1]} in context {node_id[0]}')
            else:
                ntype = self.graph.type(*node_id)
                successors = self.graph.successors(*node_id, link=Link.DEPEND_ON|Link.DELEGATE_TO)
                arg_names = []
                for n, in successors:
                    self.run(n)

                    if n[0] != node_id[0]:
                        self._initiated[node_id] = self._initiated[n]
                        return
                    else:
                        arg_names.append(n[1])
                
                args = {a: self._initiated[node_id[0], a] for a in arg_names}
                if ntype is Node.FACTORY:
                    obj = args
                else:
                    value = self.graph.value(*node_id)
                    obj = value(**args)
                self._initiated[node_id] = obj

    @property
    def results(self):
        return {k[1]: v for k, v in self._initiated.items() if k[0] == self.context}
