import pandas as pd

from .topk_indexer import TopkIndexer
from .regex_tokenizer import RegexTokenizer


class SegmentIndexer(TopkIndexer):
    
    def __init__(self, data, group_splitter=r'([^\.\n]+)', tokenizer=r'(\w+)', 
                 token_threshold=0.7, topk=5):
        super().__init__(data, tokenizer, token_threshold, topk)
        
        if isinstance(group_splitter, str):
            group_splitter = RegexTokenizer(group_splitter)
        
        self.group_splitter = group_splitter
    
    def run(self, query:str):
        query = query.lower()
        segmented_query = self.group_splitter.run(query)
        
        results = []
        for offset, q in segmented_query[['start_idx', 'token']].itertuples(index=False):
            search_results  = super().run(q)
            if len(search_results) > 0:
                query_start = search_results.index.get_level_values(0) + offset
                query_end = search_results.index.get_level_values(1) + offset
                new_indices = pd.MultiIndex.from_arrays([query_start, query_end], names=search_results.index.names[:2])
                search_results = search_results.set_index(new_indices)
                results.append(search_results)
        
        if len(results) > 0:
            results = pd.concat(results, axis=0).rename(columns={
                'text': 'original',
                'text_start': 'original_start',
                'text_end': 'original_end',
                'matching_score': 'substring_matching_score'
            })
        else:
            columns = [
                'query_start_idx', 'query_end_idx', 
                'data_index', 'original', 'original_start', 'original_end',
                'substring_matching_score', 
                'matched_len', 'coverage_score',
                'harmonic_score'
            ]
            results = pd.DataFrame(columns=columns).set_index(['query_start_idx', 'query_end_idx'])

        return results
