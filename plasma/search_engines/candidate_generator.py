import networkx as nx
import pandas as pd

from typing import NamedTuple
from scipy.stats import hmean
from ..parallel_processing.communicators import AsyncFlow, Accumulator
from ..parallel_processing.queues import ProcessQueue, TransferQueue
from ..functional import partials
from ..logging import Timer


class Segment(NamedTuple):
    candidates:set = set()
    matched_len:int = 0
    
    def generate_data(self, offset:int, path:list):
        candidates, matched_len = self
        offsets, db_path = zip(*path[offset:offset+matched_len])
        return [[dbi, c, offsets[0], offsets[-1] + 1, db_path] for dbi, c in candidates]


class generate_candidates_async(AsyncFlow):
    
    def __init__(self, position_graph:nx.DiGraph):
        super().__init__()
        
        paths = generate_paths(position_graph)
        candidate_generator = partials(generate_candidates_from_path, position_graph)
        accumulator = Accumulator(len(paths))
        self.chain(
            (ProcessQueue(8), candidate_generator),
            (candidate_generator, TransferQueue(), accumulator)
        )
        
        with self:
            for p in paths:
                self.put(p)
            candidates = sum(accumulator.wait(), [])

        self.results = combine(position_graph, candidates)


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
    candidate_data:dict[int, Segment] = {
        0: Segment()
    }
    offset = 0
    for i, n in enumerate(path):
        current_candidates, matched_len = candidate_data[offset]
        
        current_node_paths = position_graph.nodes[n]['paths']
        new_candidates = current_candidates.intersection(current_node_paths)
        
        if len(new_candidates) == 0:
            candidates = current_node_paths
            offset = i
            matched_len = 1
        else:
            candidates = new_candidates
            matched_len += 1

        candidate_data[offset] = Segment(candidates, matched_len)

    candidate_data = [s.generate_data(o, path) for o, s in candidate_data.items()]
    candidate_data = sum(candidate_data, [])
    return candidate_data


def combine(position_graph:nx.DiGraph, path_data:list):
    data = pd.DataFrame(path_data, columns=['db_index', 'db_candidate', 'start', 'end', 'db_path'])
    
    with Timer():
        data['matching_score'] = [hmean([position_graph.nodes[n]['score'] for n in  zip(range(start, end), db_path)])
                                  for start, end, db_path in data[['start', 'end', 'db_path']].itertuples(index=False)]

    return data
