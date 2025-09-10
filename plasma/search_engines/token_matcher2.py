import networkx as nx
import pandas as pd
import difflib

from ..functional import AutoPipe


class TokenMatcher(AutoPipe):

    def __init__(self, graph: nx.DiGraph, threshold):
        super().__init__()

        self._graph = graph
        self.threshold = threshold
    
    def run(self, tokens:list[str]):
        matches = []
        for i, tk in enumerate(tokens):
            for db_tk in self._graph.nodes:
                score = difflib.SequenceMatcher(None, tk, db_tk).ratio()
                if score >= self.threshold:
                    matches.append([i, tk, db_tk, score])

        return pd.DataFrame(matches, columns=['offset', 'token', 'db_token', 'score'])\
                    .set_index(['offset', 'token']).sort_index()
