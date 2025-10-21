import networkx as nx
import pandas as pd

from typing import NamedTuple
from scipy.stats import hmean


class Segment(NamedTuple):
    offset:int = None
    args:set = set()
    matched_len:int = 0
    
    def generate_data(self, path:list):
        offset, args, matched_len = self
        offsets, token_path = zip(*path[offset:offset+matched_len])
        return [[a, offsets[0], offsets[-1] + 1, token_path] for a in args]
    
    def update(self, new_paths:set):
        return Segment(
            self.offset,
            new_paths,
            self.matched_len + 1,
        )
    
    @property
    def empty(self):
        return len(self.args) == 0


def generate_candidates(position_graph:nx.DiGraph):
    paths = generate_paths(position_graph)
    candidates = [generate_candidates_from_path(position_graph, p) for p in paths]
    candidates = sum(candidates, [])
    return combine(position_graph, candidates)
        

def generate_paths(position_graph:nx.DiGraph):
    roots = [n for n in position_graph if position_graph.in_degree(n) == 0]
    leaves = [n for n in position_graph if position_graph.out_degree(n) == 0]
    paths = []
    for r in roots:
        paths.extend(nx.all_simple_paths(position_graph, r, leaves))
    return paths


def generate_candidates_from_path(position_graph:nx.DiGraph, path):
    candidates = [Segment()]
    for i, (curr, next) in enumerate(zip(path[:-1], path[1:])):
        path_args = position_graph.edges[curr, next]['path_args']
        if candidates[-1].empty:
            candidates[-1] = Segment(i, path_args, 2)
        else:
            current_args = candidates[-1].args
            new_args = current_args.intersection(path_args)
        
            if len(new_args) == 0:
                candidates.append(Segment(i, path_args, 2))
            else:
                candidates[-1] = candidates[-1].update(new_args)

    candidate_data = [s.generate_data(path) for s in candidates if not s.empty]
    candidate_data = sum(candidate_data, [])
    return candidate_data


def combine(position_graph:nx.DiGraph, path_data:list):
    data = pd.DataFrame(path_data, columns=['db_index', 'start', 'end', 'db_path'])
    
    data['matching_score'] = [hmean([position_graph.nodes[n]['score'] for n in  zip(range(start, end), db_path)]) 
                              for start, end, db_path in data[['start', 'end', 'db_path']].itertuples(index=False)]

    return data
