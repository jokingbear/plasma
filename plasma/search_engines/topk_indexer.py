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
                    [find_match(self._path_token_maps, db_path, db_candidate) 
                    for db_path, db_candidate in db_matches],
                    columns=['text_start', 'text_end', 'matched_len']
                )
        results = pd.concat([results, matches], axis=1)
        
        # calculcate scores
        coverage_scores = results['matched_len'] / results['db_candidate'].map(len)
        results['coverage_score'] = coverage_scores.values
        results['harmonic_score'] = hmean(results[['matching_score', 'coverage_score']].values, axis=1)
        
        # group and get topk
        results = results\
                    .groupby(['query_start_idx', 'query_end_idx'])\
                        .apply(
                            sort_candidate, 
                            topk=self.topk, full_data=self._data,
                            include_groups=False
                        )
        return results


def find_match(path_token_maps:dict[tuple, pd.DataFrame], db_path, db_candidate):
    _, offset, size = difflib.SequenceMatcher(None, db_path, db_candidate).find_longest_match()
    start = path_token_maps[db_candidate].iloc[offset]['start_idx']
    end = path_token_maps[db_candidate].iloc[offset + size - 1]['end_idx'] 
    
    return start, end, size


def sort_candidate(df:pd.DataFrame, topk, full_data:pd.DataFrame):
    columns = [
        'data_index', 'text', 'text_start', 'text_end', 
        'matching_score', 'matched_len', 'coverage_score', 'harmonic_score'
    ]
    
    new_frame = df.sort_values(['matching_score', 'coverage_score'], ascending=False)\
                    .rename(columns={'db_index': 'data_index'})\
                        .iloc[:topk].copy()

    new_frame['text'] = full_data.iloc[new_frame['data_index'].values]['text'].values
    return new_frame[columns]
