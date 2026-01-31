import plasma.functional as F
import pandas as pd

from typing import Iterable
from .index import Index
from .regex_tokenizer import RegexTokenizer
from .inquirer import PathInquirer
from .token_matcher import TokenMatcher


class GraphIndexer(F.AutoPipe[[str], pd.DataFrame]):
    
    def __init__(self, 
                data:list[str],
                group_splitter=r'[^\.\n]+', tokenizer=r'\w+',
                token_threshold=0.7, topk=5,
            ):
        super().__init__()
        
        tokenizer = RegexTokenizer(tokenizer)
        index = Index(data, tokenizer)
        token_matcher = TokenMatcher(index, token_threshold)
        
        self._index = index
        self.context_splitter = RegexTokenizer(group_splitter)
        self.path_inquirer = PathInquirer(self._index, tokenizer, token_matcher, topk)
    
    def run(self, query:str):
        contexts = self.context_splitter(query)
        data = []
        for start, end, context in contexts.itertuples(index=False):
            matches = self.path_inquirer(context)
            if len(matches) > 0:
                match_frame = pd.DataFrame(matches)
                match_frame['qchar_start'] = match_frame['qchar_start'] + start
                data.append(match_frame)
        
        if len(data) > 0:
            data = pd.concat(data, axis=0, ignore_index=True).rename(columns=column_map)
        else:
            columns = [
                'query_start_idx', 'query_end_idx',
                'data_index', 'original_start', 'original_end', 'original',
                'substring_matching_score', 'coverage_score',
                'matched_len', 'harmonic_score'
            ]
            data = pd.DataFrame(columns=columns)
        
        return data.set_index(['query_start_idx', 'query_end_idx']).sort_index()


column_map = {
    'qchar_start': 'query_start_idx',
    'qchar_end': 'query_end_idx',
    'db_arg': 'data_index',
    'db_char_start': 'original_start',
    'db_char_end': 'original_end',
    'db_value':'original',
    'matching_score': 'substring_matching_score',
}
