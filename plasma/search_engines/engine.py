import plasma.functional as F
import pandas as pd

from .index import Index
from .regex_tokenizer import RegexTokenizer
from .inquirer import PathInquirer, Match
from .token_matcher import TokenMatcher
from ..functional.helpers.color_printer import Color
from ..data_model.collections import Stream


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
    
    def run(self, query:str, return_frame=True):
        contexts = self.context_splitter(query)
        data = list[Match]()
        for start, end, context in contexts.itertuples(index=False):
            matches = self.path_inquirer(context).select(lambda m:m.update(start))
            data.extend(matches)
        
        if return_frame:
            print(Color.YELLOW.render(f'frame will be deprecated in the future, please set it to false'))
            columns = [
                'query_start_idx', 'query_end_idx',
                'data_index', 'original_start', 'original_end', 'original',
                'substring_matching_score', 'coverage_score',
                'matched_len', 'harmonic_score'
            ]
            return pd.DataFrame(data, columns=columns).set_index(['query_start_idx', 'query_end_idx']).sort_index()
        
        return Stream(data).sort(lambda m: (m.qchar_start, m.qchar_end))
