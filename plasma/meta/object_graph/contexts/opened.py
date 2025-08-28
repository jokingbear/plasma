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
        
        checker = GraphChecker(self.graph, self.name)
        fields = set()
        for n in names:
            checker.run(self.name, n)
            fields.update(checker.results)
        
        field_values = pd.Series({node_id: self.graph.value(*node_id, default=self.requirement) 
                                  for node_id in fields})
        field_values = field_values.sort_index()
        
        results = {}
        for k in field_values.index.get_level_values(0).unique():
            if k == self.name:
                results.update(field_values.loc[k])
            else:
                results[k] = field_values.loc[k].to_dict()
        
        return BeautifulDict(results)


class GraphChecker:
    
    def __init__(self, graph:ContextGraph, context):
        super().__init__()

        self.graph = graph
        self.context = context
        self._state = set()
    
    def run(self, context, name):
        node_id = context, name
        ntype = self.graph.type(*node_id)
        if ntype in Node.LEAF|Node.SINGLETON:
            self._state.add(node_id)
        else:
            successors = self.graph.successors(*node_id, link=None)
            for n, in successors:
                self.run(*n)

    @property
    def results(self):
        return self._state


class Required: pass


class BeautifulDict(dict):
    
    def __iter__(self):
        for v in self.values():
            yield v
    
    def __repr__(self):
        text = json.dumps(self, indent=2, default=lambda _: Required.__name__)
        text = text.replace(f'"{Required.__name__}"', Required.__name__)
        return text
