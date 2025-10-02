import plasma.functional as F
import pandas as pd
import networkx as nx
import itertools as iter

from .regex_tokenizer import RegexTokenizer
from .token_matcher2 import TokenMatcher
from .token_graph import TokenGraph
from scipy.stats import hmean
from ..parallel_processing.communicators import AsyncFlow, Accumulator
from ..parallel_processing.queues import ProcessQueue, TransferQueue
from .candidate_generator import generate_candidates_async, generate_candidates


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
        
        columns = ['query_start_idx', 'query_end_idx', 'db_path', 'db_index', 'db_candidate', 'matching_score']
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
