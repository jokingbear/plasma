import networkx as nx
import pandas as pd

from .readable_manager import ReadableManager
from warnings import deprecated


@deprecated('this class is deprecated, use ContextManager instead')
class Manager(ReadableManager):
    
    def run(self, *names, **init_args):
        assert len(names) > 0, 'there must be at least one component'
        
        objs = init_args.copy()
        for n in names:
            init_objects(self._dep_graph, n, objs)

        return pd.Series({n: objs[n] for n in names})


def init_objects(graph:nx.DiGraph, key, objs:dict):
    node_attr = graph.nodes[key]
    if key not in objs:
        if 'value' in node_attr:
            objs[key] = node_attr['value']
        elif 'factory' in node_attr:
            objs[key] = {}
            for child in graph.successors(key):
                init_objects(graph, child, objs)
                objs[key][child] = objs[child]
        else:
            args = {}
            for child in graph.successors(key):
                init_objects(graph, child, objs)
                args[child] = objs[child]
            
            try:
                objs[key] = node_attr['initiator'](**args)
            except KeyError as e:
                raise RuntimeError(key) from e
