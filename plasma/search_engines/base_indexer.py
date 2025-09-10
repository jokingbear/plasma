import plasma.functional as F
import pandas as pd
import networkx as nx
import numpy as np
import itertools as iter

from .regex_tokenizer import RegexTokenizer
from .token_matcher2 import TokenMatcher
from .path_set_walker2 import PathWalker
from .token_graph import TokenGraph
from scipy.stats import hmean


class BaseIndexer(TokenGraph, F.AutoPipe):
    
    def __init__(self, data:list[str], tokenizer=r'(\w+)', token_threshold=0.7):
        tokenizer = RegexTokenizer(tokenizer)
        F.AutoPipe.__init__(self)
        TokenGraph.__init__(self, data, tokenizer)
        
        self.token_matcher = TokenMatcher(self._graph, token_threshold)

    def run(self, query:str):
        query = query.lower()
        token_data = self.tokenizer.run(query)
        db_token_matching_data = self.token_matcher.run(token_data['token'])
        
        subgraph = self._graph.subgraph(db_token_matching_data['db_token'])
        position_graph = build_position_graph(subgraph, db_token_matching_data)
        candidates  = generate_candidates(position_graph)
        
        candidates['query_start_idx'] = token_data.iloc[candidates['start'].values]['start_idx'].values
        candidates['query_end_idx'] = token_data.iloc[candidates['end'].values - 1]['end_idx'].values
        
        columns = ['query_start_idx', 'query_end_idx', 'db_path', 'db_candidate', 'matching_score']
        return candidates[columns]


def build_position_graph(db_graph:nx.DiGraph, token_matching_data:pd.DataFrame):
    position_graph = nx.DiGraph()
    grouped = {offset: df[['db_token', 'score']] for offset, df in token_matching_data.groupby('offset')}

    sorted_offsets = sorted(token_matching_data.index.get_level_values('offset').unique())
    for o in sorted_offsets:
        df:pd.DataFrame = token_matching_data.loc[o]
        for db_token, score in df[['db_token', 'score']].itertuples(index=False):
            position_graph.add_node((o, db_token), score=score, paths=db_graph.nodes[db_token]['paths'])

    for o in sorted_offsets:
        o_tokens = token_matching_data.loc[o]['db_token']
        next_o = o + 1
        token_matching_data.loc
        next_tokens = grouped.get(next_o, {'db_token': []})['db_token']

        for otk, ntk in iter.product(o_tokens, next_tokens):
            if (otk, ntk) in db_graph.edges:
                position_graph.add_edge((o, otk), (next_o, ntk))

    return position_graph


def generate_candidates(position_graph:nx.DiGraph):
    final_candidates = []
    scores = pd.Series({n:score for n, score in position_graph.nodes(data='score')})
    for c in nx.connected_components(position_graph.to_undirected()):
        if len(c) > 1:
            sub_position_graph:nx.DiGraph = position_graph.subgraph(c)
            solve_components(sub_position_graph, final_candidates)
        else:
            node, = list(c)
            solve_singleton(position_graph, node, final_candidates)

    final_candidates = pd.DataFrame(final_candidates, columns=['start', 'end', 'db_path', 'db_candidate'])
    candidate_scores = [hmean(scores.loc[zip(range(start, end), db_path)]) 
                        for start, end, db_path in final_candidates[['start', 'end', 'db_path']].itertuples(index=False)]
    final_candidates['matching_score'] = candidate_scores
    return final_candidates


def solve_components(position_graph:nx.DiGraph, final_candidates:list):
    roots = [n for n in position_graph if position_graph.in_degree(n) == 0]
    leaves = [n for n in position_graph if position_graph.out_degree(n) == 0]
    paths = iter.chain(*[nx.all_simple_paths(position_graph, r, leaves) for r in roots])
    
    for p in paths:
        candidate_counts, candidate_offsets = generate_candicate_stats(p, position_graph)                
        
        for k, c in candidate_counts.items():
            if c > 1:
                offset = candidate_offsets[k]
                start, _ = p[offset]
                end, _ = p[offset + c]
                end += 1
                _, db_path = zip(*p[offset:offset + c + 1])
                final_candidates.append([start, end, db_path, k])


def generate_candicate_stats(path, position_graph:nx.DiGraph):
    candidate_counts = {}
    candidate_offsets = {}
                
    for i, n in enumerate(path[:-1]):
        candiates:set = position_graph.nodes[n]['paths']
        next_candidates:set = position_graph.nodes[path[i + 1]]['paths']
        intersection = candiates.intersection(next_candidates)
        for candidate_path in intersection:
            candidate_counts[candidate_path] = candidate_counts.get(candidate_path, 0) + 1
            candidate_offsets[candidate_path] = candidate_offsets.get(candidate_path, i)
    
    return candidate_counts, candidate_offsets


def solve_singleton(graph:nx.DiGraph, node, final_candidates:list):
    node_attr = graph.nodes[node]
    candidates = node_attr['paths']
    start, db_token = node
    
    for c in candidates:
        final_candidates.append([start, start + 1, (db_token,), c])
