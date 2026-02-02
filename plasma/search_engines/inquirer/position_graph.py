import networkx as nx
import pandas as pd
import itertools

from ..index import Index
from .position_path import PositionPath


class PositionGraph(nx.DiGraph):
    
    def __init__(self, index:Index, qtoken_frame:pd.DataFrame, qtoken_2_dbtokens:dict[str, dict[str, float]]):
        super().__init__()
        
        for i, qtoken in qtoken_frame['token'].items():
            db_tokens = qtoken_2_dbtokens.get(qtoken, {})
            self.add_nodes_from(((i, dbtk), {'score': score}) for dbtk, score in db_tokens.items())
        
        for i, qtoken in qtoken_frame['token'].iloc[:-1].items():
            next_qtoken = qtoken_frame.iloc[i + 1]['token']

            current_db_tokens = qtoken_2_dbtokens.get(qtoken, {})
            next_db_tokens = qtoken_2_dbtokens.get(next_qtoken, {})
            self.add_edges_from(
                ((i, curr_dbtoken), (i + 1, next_dbtoken)) 
                for curr_dbtoken, next_dbtoken in itertools.product(current_db_tokens, next_db_tokens)
                if index.has_pair(curr_dbtoken, next_dbtoken)
            )
    
    def generate_paths(self):
        roots = (n for n in self if self.in_degree(n) == 0)
        leaves = [n for n in self if self.out_degree(n) == 0]

        for r in roots:
            for p in nx.all_simple_paths(self, r, leaves):
                yield PositionPath(p)
