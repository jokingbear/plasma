import pandas as pd
import networkx as nx

from .regex_tokenizer import RegexTokenizer


class TokenGraph:
    
    def __init__(self, data:list[str], tokenizer:RegexTokenizer):        
        assert len(data) == len(set(data)), 'data is not unique'
        
        self.tokenizer = tokenizer

        tokenized_data, tokenized_offsets = tokenize_data(data, tokenizer)
        graph = build_graph(tokenized_data)
        self._data = tokenized_data
        self._tokenized_offsets = tokenized_offsets
        self._graph = graph


def tokenize_data(data:list[str], tokenizer:RegexTokenizer):
    tokenized_offsets = {}
    tokenized_data = []
    for i, txt in enumerate(data):
        token_frame = tokenizer.run(txt.lower())
        path = tuple(token_frame['token'].tolist())
        tokenized_data.append([i, txt, path])
        tokenized_offsets[path] = token_frame
    
    return pd.DataFrame(tokenized_data, columns=['data_index', 'text', 'path']), tokenized_offsets
    

def build_graph(tokenized_data:pd.DataFrame):
    graph = nx.DiGraph()
    
    for path in tokenized_data['path']:
        nx.add_path(graph, path)
        
        for tk in path:
            paths:set = graph.nodes[tk].get('paths', set())
            paths.add(path)
            graph.add_node(tk, paths=paths)

    return graph
