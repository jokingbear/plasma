import difflib
import numpy as np
import pandas as pd

from .overlap_filter_indexer import OverlapFilterIndexer
from scipy.stats import hmean


class TopkIndexer(OverlapFilterIndexer):
    
    def __init__(self, data, tokenizer=r'(\w+)', token_threshold=0.7, topk=5):
        super().__init__(data, tokenizer, token_threshold)
        
        self.topk = topk
    
    def run(self, query) -> pd.DataFrame:
        results = super().run(query)
        
        # find matching block in db path
        db_matches = results[['db_path', 'db_candidate']].itertuples(index=False)
        matches = pd.DataFrame(
                    [find_match(self._tokenized_offsets, db_path, db_candidate) 
                    for db_path, db_candidate in db_matches],
                    columns=['text_start', 'text_end', 'matched_len']
                )
        results = pd.concat([results, matches], axis=1)
        
        # calculcate scores
        coverage_scores = results['matched_len'] / results['db_candidate'].map(len)
        results['coverage_score'] = coverage_scores.values
        results['harmonic_score'] = hmean(results[['matching_score', 'coverage_score']].values, axis=1)
        
        # group and get topk
        results = results.merge(self._data, left_on='db_candidate', right_on='path')
        results = results.groupby(['query_start_idx', 'query_end_idx']).apply(sort_candidate, topk=self.topk, 
                                                                              include_groups=False)
        return results


def find_match(tokenized_offsets:dict[tuple, pd.DataFrame], db_path, db_candidate):
    _, offset, size = difflib.SequenceMatcher(None, db_path, db_candidate).find_longest_match()
    start = tokenized_offsets[db_candidate].iloc[offset]['start_idx']
    end = tokenized_offsets[db_candidate].iloc[offset + size - 1]['end_idx'] 
    
    return start, end, size


def sort_candidate(df:pd.DataFrame, topk):
    columns = [
        'data_index', 'text', 'text_start', 'text_end', 
        'matching_score', 'matched_len', 'coverage_score', 'harmonic_score'
    ]
    return df[columns].sort_values('harmonic_score', ascending=False).reset_index(drop=True).iloc[:topk]
