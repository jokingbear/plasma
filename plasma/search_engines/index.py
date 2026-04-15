import pandas as pd
import networkx as nx

from typing import Callable, Iterable, NamedTuple, Sequence
from collections import defaultdict

from ..data_model.collections import Stream


class Index:
    
    def __init__(self, data:Sequence[str], tokenizer:Callable[[str], pd.DataFrame]):
        assert len(data) == len(set(data)), 'data must be unique'
        
        token2positions = defaultdict[str, dict[TokenPosition, tuple[int, int]]](dict)
        graph = nx.DiGraph()
        path_args = {}
        paths:list[tuple[str]] = []
        for i, d in enumerate(data):
            token_frame = tokenizer(d.lower())
            path = tuple(token_frame['token'])
            for token_arg, start, end, token in token_frame.itertuples(index=True):
                position = TokenPosition(i, token_arg)
                token2positions[token][position] = start, end
            
            nx.add_path(graph, path)
            path_args[path] = i
            paths.append(path)
        
        self._token2positions = token2positions
        self._graph = graph
        self._paths = paths
        self._data = data
    
    def get_path_args(self, token:str) -> Stream[int]:
        positions = self._token2positions.get(token, {})
        return Stream(p.path_arg for p in positions)
    
    def get_char_interval(self, token:str, path_arg:int, token_offset:int):
        position = TokenPosition(path_arg, token_offset)
        return self._token2positions[token][position]
    
    def has_pair(self, token:str, next_token:str):
        return (token, next_token) in self._graph.edges

    def get_path(self, arg:int):
        return self._paths[arg]
    
    def get_data(self, arg:int):
        return self._data[arg]

    @property
    def tokens(self) -> Iterable[str]:
        for token in self._token2positions:
            yield token


class TokenPosition(NamedTuple):
    path_arg:int
    token_arg:int
