import pandas as pd
import json

from .renderable import RenderableContext
from typing import Hashable
from ..context_graph import ContextGraph
from ..types import Node


class OpenedContext(RenderableContext):
    
    def __init__(self, graph, name):
        super().__init__(graph, name)
    
        self.requirement = Required
    
    def inputs(self, *names:Hashable):
        for n in names:
            assert (self.name, n) in self.graph
        
        results = {}
        for n in names:
            checker = GraphChecker(self.graph, self.name, n)
            checker.run()
            results.update(checker.results)
        
        return BeautifulDict(results)


class GraphChecker:
    
    def __init__(self, graph:ContextGraph, context, name):
        super().__init__()

        self.graph = graph
        self.context = context
        self.name = name
        
        initiated = {}
        self._state = initiated
    
    def run(self, node_id=None):
        node_id = node_id or (self.context, self.name)
        ntype = self.graph.type(*node_id)
        if node_id[0] != self.context:
            checker = GraphChecker(self.graph, *node_id)
            checker.run()
            
            other_context = self._state.get(node_id[0], {})
            other_context.update(checker.results)
            
            self._state[node_id[0]] = other_context
        elif ntype in Node.LEAF|Node.SINGLETON:
            self._state[node_id[1]] = self.graph.value(*node_id, default=Required)
        else:
            successors = self.graph.successors(*node_id, link=None)
            for n, in successors:
                self.run(n)

    @property
    def results(self):
        return BeautifulDict(self._state)


class Required: pass


class BeautifulDict(dict):
    
    def __iter__(self):
        for v in self.values():
            yield v
    
    def __repr__(self):
        text = json.dumps(self, indent=2, default=lambda _: Required.__name__)
        text = text.replace(f'"{Required.__name__}"', Required.__name__)
        return text
