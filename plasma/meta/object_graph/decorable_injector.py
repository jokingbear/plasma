import plasma.functional as F
import networkx as nx
import pandas as pd

from typing import Callable


class DependencyInjector(F.AutoPipe):
    
    def __init__(self, wrapper:Callable[[str, object], object]=None):
        super().__init__()
        
        self.wrapper = wrapper
    
    def run(self, object_graph:nx.DiGraph, *names:str, **init_args) -> dict:
        if len(names) == 0:
            names = object_graph.nodes
        
        names = list(names)
        object_dict = {}
        for n in names:
            _recursive_init(object_graph, self.wrapper, n, object_dict, init_args)
                
        return pd.Series({n: object_dict.get(n, _NotInitialized) for n in names}).loc[names]


class _NotInitialized:
    pass


def _recursive_init(object_graph:nx.DiGraph, wrapper, key, object_dict:dict, init_args:dict):
    if key not in object_dict and key in object_graph:
        if 'value' in object_graph.nodes[key]:
            obj = object_graph.nodes[key]['value']
            object_dict[key] = wrapper(key, obj)
        else:
            arg_maps = {}
            for arg in object_graph.neighbors(key):
                if arg in init_args:
                    arg_object = init_args[arg]
                else:
                    node_attributes = object_graph.nodes[arg]
                    if 'value' in node_attributes:
                        arg_object = node_attributes['value']
                    else:
                        _recursive_init(object_graph, wrapper, arg, object_dict, init_args)
                        arg_object = object_dict.get(arg, _NotInitialized)

                if arg_object is _NotInitialized:
                    error_message = f'{arg} is not in init_args or dependency graph at key: {key}'
                    raise KeyError(error_message)

                arg_maps[arg] = arg_object

            if len(arg_maps) == object_graph.out_degree(key):
                try:
                    obj = object_graph.nodes[key]['initiator'](**arg_maps)
                    if wrapper is not None:
                        obj = wrapper(key, obj)
                    object_dict[key] = obj
                except Exception as e:
                    raise RuntimeError(f'error at {key}') from e
