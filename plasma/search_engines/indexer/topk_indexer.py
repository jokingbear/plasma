import difflib
import numpy as np
import pandas as pd

from .offset_refiner import OffsetRefiner
from scipy.stats import hmean


class TopkIndexer(OffsetRefiner):
    
    def __init__(self, data, tokenizer=r'(\w+)', token_threshold=0.7, topk=5):
        super().__init__(data, tokenizer, token_threshold)
        
        self.topk = topk
    
    def run(self, query) -> pd.DataFrame:
        results = super().run(query)
        
        # calculcate scores
        coverage_scores = results['matched_len'] / results['db_candidate'].map(len)
        results['coverage_score'] = coverage_scores.values
        
        if len(results) > 0:
            results['harmonic_score'] = hmean(results[['matching_score', 'coverage_score']].values, axis=1)
        else:
            results['harmonic_score'] = []
        
        # group and get topk
        results = results\
                    .groupby(['start', 'end'])\
                        .apply(
                            sort_candidate, 
                            topk=self.topk, 
                            include_groups=False
                        )
        return results


def sort_candidate(df:pd.DataFrame, topk):
    columns = [
        'db_index', 'db_candidate', 'db_start', 'db_end', 
        'matching_score', 'matched_len', 'coverage_score', 'harmonic_score'
    ]
    
    new_frame = df.sort_values(['matching_score', 'coverage_score'], ascending=False)
    new_frame = new_frame.iloc[:topk]
    return new_frame[columns]
