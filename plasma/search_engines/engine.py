import pandas as pd

from typing import Any, Sequence
from warnings import deprecated
from .index import Index
from .regex_tokenizer import RegexTokenizer
from .inquirer import PathInquirer
from .token_matcher import TokenMatcher
from ..data_model.collections import ZippedStream
from ..functional import ReadableClass


@deprecated(
    'this class is deprecated, use StreamIndex for better data model supports',
    stacklevel=2
)
class GraphIndexer(ReadableClass):
    
    def __init__(
            self, 
            data:Sequence[str],
            group_splitter=r'[^\.\n]+', tokenizer=r'\w+',
            token_threshold=0.7, topk=5,
        ):
        super().__init__()
        
        tokenizer = RegexTokenizer(tokenizer)
        index = Index(data, tokenizer)
        token_matcher = TokenMatcher(index, token_threshold, topk)
        
        self._index = index
        self.context_splitter = RegexTokenizer(group_splitter)
        self.path_inquirer = PathInquirer(self._index, tokenizer, token_matcher)
        self.topk = topk
    
    def run(self, query:str):
        contexts = self.context_splitter(query)
        data = (
            ZippedStream[int, int, str](contexts.itertuples(index=False))
            .unwind(lambda start, end, context:
                self.path_inquirer(context)
                .select(lambda m: m.update(start))
            ).split(lambda m:
                (
                    m.query.start, m.query.end,
                    m.db.arg, m.db.start, m.db.end, m.db.value, 
                    m.score.substring, m.score.coverage,
                    m.score.token_len, m.score.harmonic
                )
            )
        )
        
        columns = [
            'query_start_idx', 'query_end_idx',
            'data_index', 'original_start', 'original_end', 'original',
            'substring_matching_score', 'coverage_score',
            'matched_len', 'harmonic_score'
        ]
        
        unique_columns = ['query_start_idx', 'query_end_idx', 'data_index', 'original_start', 'original_end']
        sort_columns = ['query_start_idx', 'query_end_idx', 'substring_matching_score', 'matched_len', 'harmonic_score']
        return (
            pd.DataFrame(data, columns=columns)
            .drop_duplicates(subset=unique_columns)
            .set_index(['query_start_idx', 'query_end_idx'])
            .sort_values(sort_columns,ascending=[True, True, False, False, False])
        )

    def __call__(self, query:str):
        return self.run(query)
