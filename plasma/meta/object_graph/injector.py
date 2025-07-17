import plasma.functional as F
import networkx as nx
import pandas as pd


class DependencyInjector(F.AutoPipe):
    
    def __init__(self, object_graph:nx.DiGraph):
        super().__init__()
        
        self.object_graph = object_graph
    
    def run(self, *names, **init_args) -> dict:
        if len(names) == 0:
            names = self.object_graph.nodes
        
        names = list(names)
        object_dict = {}
        for n in names:
            _recursive_init(self.object_graph, n, object_dict, init_args)
                
        return pd.Series({n: object_dict.get(n, _NotInitialized) for n in names}).loc[names]


class _NotInitialized:
    pass


def _recursive_init(object_graph:nx.DiGraph, key, object_dict:dict, init_args:dict):
    if key not in object_dict and key in object_graph:
        if 'value' in object_graph.nodes[key]:
            object_dict[key] = object_graph.nodes[key]['value']
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
                        _recursive_init(arg, object_dict, init_args)
                        arg_object = object_dict.get(arg, _NotInitialized)

                if arg_object is _NotInitialized:
                    error_message = f'{arg} is not in init_args or dependency graph at key: {key}'
                    raise KeyError(error_message)

                arg_maps[arg] = arg_object

            if len(arg_maps) == object_graph.out_degree(key):
                try:
                    object_dict[key] = object_graph.nodes[key]['initiator'](**arg_maps)
                except Exception as e:
                    raise RuntimeError(f'error at {key}') from e
