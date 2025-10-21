import pandas as pd
import networkx as nx

from .regex_tokenizer import RegexTokenizer


class TokenGraph:
    
    def __init__(self, data:list[str], tokenizer:RegexTokenizer):        
        assert len(data) == len(set(data)), 'data is not unique'
        
        self.tokenizer = tokenizer

        tokenized_data, tokenized_offsets, graph = tokenize_data(data, tokenizer)
        self._data = tokenized_data
        self._path_token_maps = tokenized_offsets
        self._graph = graph


def tokenize_data(data:list[str], tokenizer:RegexTokenizer):
    path_token_maps = {}
    path_data = []
    graph = nx.DiGraph()
    for pid, txt in enumerate(data):
        token_frame = tokenizer.run(txt.lower())
        path = tuple(token_frame['token'].tolist())
        insert_path(graph, pid, path)
        path_data.append([txt, path])
        path_token_maps[path] = token_frame
        
    return pd.DataFrame(path_data, columns=['text', 'path']), path_token_maps, graph
    

def insert_path(graph:nx.DiGraph, path_id, path:list):
    for start, end in zip(path[:-1], path[1:]):
        graph.add_edge(start, end)
        paths:set = graph.edges[start, end].get('path_args', set())
        paths.add(path_id)
        graph.edges[start, end]['path_args'] = paths
