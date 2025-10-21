import plasma.functional as F
import pandas as pd
import networkx as nx
import itertools as iter

from .regex_tokenizer import RegexTokenizer
from .token_matcher2 import TokenMatcher
from .token_graph import TokenGraph
from .candidate_generator import generate_candidates


class BaseIndexer(TokenGraph, F.AutoPipe):
    
    def __init__(self, data:list[str], tokenizer=r'(\w+)', token_threshold=0.7):
        tokenizer = RegexTokenizer(tokenizer)
        F.AutoPipe.__init__(self)
        TokenGraph.__init__(self, data, tokenizer)
        
        self.token_matcher = TokenMatcher(self._graph, token_threshold)

    def run(self, query:str):
        query = query.lower()
        token_data = self.tokenizer.run(query)
        q2db_token_maps = self.token_matcher.run(token_data['token'])
        
        subgraph = self._graph.subgraph(q2db_token_maps['db_token'])
        position_graph = build_position_graph(subgraph, q2db_token_maps)
        path_candidate_data  = generate_candidates(position_graph)
        path_candidate_data['db_candidate'] = self._data.iloc[path_candidate_data['db_index'].values]['path'].values
        path_candidate_data['query_start_idx'] = token_data.iloc[path_candidate_data['start'].values]['start_idx'].values
        path_candidate_data['query_end_idx'] = token_data.iloc[path_candidate_data['end'].values - 1]['end_idx'].values
        
        columns = ['query_start_idx', 'query_end_idx', 'db_path', 'db_index', 'db_candidate', 'matching_score']
        return path_candidate_data[columns]


def build_position_graph(db_graph:nx.DiGraph, q2db_token_maps:pd.DataFrame):
    position_graph = nx.DiGraph()
    grouped = {q_offset: df[['db_token', 'score']] for q_offset, df in q2db_token_maps.groupby('offset')}

    sorted_offsets = sorted(q2db_token_maps.index.get_level_values('offset').unique())
    for o in sorted_offsets:
        df:pd.DataFrame = q2db_token_maps.loc[o]
        for db_token, score in df[['db_token', 'score']].itertuples(index=False):
            position_graph.add_node((o, db_token), score=score)

    for o in sorted_offsets:
        curr_tokens = q2db_token_maps.loc[o]['db_token']
        next_o = o + 1
        next_tokens = grouped.get(next_o, {'db_token': []})['db_token']

        for ctk, ntk in iter.product(curr_tokens, next_tokens):
            if (ctk, ntk) in db_graph.edges:
                path_args = db_graph.edges[ctk, ntk]['path_args']
                position_graph.add_edge((o, ctk), (next_o, ntk), path_args=path_args)

    return position_graph
