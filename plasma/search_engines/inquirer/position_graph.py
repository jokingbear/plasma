import networkx as nx
import pandas as pd
import itertools

from .position_path import PositionPath
from ..index import Index
from ...data_model.collections import Stream


class PositionGraph(nx.DiGraph):
    
    def __init__(self, index:Index, qtoken_frame:pd.DataFrame, qtoken_2_dbtokens:dict[str, dict[str, float]]):
        super().__init__()
        
        for i, qtoken in qtoken_frame['token'].items():
            db_tokens = qtoken_2_dbtokens.get(qtoken, {})
            self.add_nodes_from(((i, dbtk), {'score': score}) for dbtk, score in db_tokens.items())
        
        sequences = zip(qtoken_frame['token'].iloc[:-1], qtoken_frame['token'].iloc[1:])
        for i, (qtoken, next_qtoken) in enumerate(sequences):
            current_db_tokens = qtoken_2_dbtokens.get(qtoken, {})
            next_db_tokens = qtoken_2_dbtokens.get(next_qtoken, {})
            self.add_edges_from(
                ((i, curr_dbtoken), (i + 1, next_dbtoken)) 
                for curr_dbtoken, next_dbtoken in itertools.product(current_db_tokens, next_db_tokens)
                if index.has_pair(curr_dbtoken, next_dbtoken)
            )
    
    def generate_paths(self):
        return (
            Stream(nx.connected_components(self.to_undirected()))
            .split(lambda c:(
                    [n for n in c if self.in_degree(n) == 0],
                    [n for n in c if self.out_degree(n) == 0]
                )
            ).unwind(lambda rs, ls:
                Stream(rs)
                .unwind(lambda r: nx.all_simple_paths(self, r, ls))
                .select(lambda p:
                    PositionPath(
                        p,
                        {n[1]: self.nodes[n]['score'] for n in p}
                    )
                )
            )
        )

