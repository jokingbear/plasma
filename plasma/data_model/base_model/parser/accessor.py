import networkx as nx
import re


class AccessorInitGraph(nx.DiGraph):
    
    def __init__(self, accessors:dict[str, object]):
        super().__init__()
        
        for k, v in accessors.items():
            chain = k.split('.')
            chain = [_standardize(c) for c in chain]
            nodes = [tuple(chain[:i + 1]) for i in range(len(chain))]
            nx.add_path(self, nodes)
            
            self.add_edge('', nodes[0])
            self.add_node(nodes[-1], value=v)


def _standardize(accessor:str):
    if re.search(r'^\d+$', accessor) is not None:
        return int(accessor)
    else:
        return accessor
