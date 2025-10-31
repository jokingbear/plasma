import numpy as np
import pandas as pd

from .base import BaseIndexer


class OverlapFilterIndexer(BaseIndexer):
    
    def run(self, query) -> pd.DataFrame:
        search_results = super().run(query)
        intervals = search_results.groupby(['start', 'end']).count()['db_path']
        
        start = search_results['start'].values
        end = search_results['end'].values
        
        bound_condition = (start[np.newaxis] <= start[:, np.newaxis]) & (end[:, np.newaxis] <= end[np.newaxis])
        bound_condition = bound_condition.sum(axis=1)
        min_thresholds = intervals.loc[search_results[['start', 'end']].itertuples(index=False)].values
                
        return search_results[bound_condition == min_thresholds].reset_index(drop=True)
