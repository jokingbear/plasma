import difflib
import pandas as pd

from ...functional import auto_map_func
from .overlap_filter import OverlapFilterIndexer


class OffsetRefiner(OverlapFilterIndexer):
    
    def run(self, query):
        results = super().run(query)
        
        block_finder = auto_map_func(find_match_block)
        matches = [*map(block_finder, results[['start', 'db_path', 'db_candidate']].itertuples(index=False))]
        matches = pd.DataFrame(matches, columns=[
            'start', 'end',
            'db_start', 'db_end',
            'matched_len'
        ])
        updated_results = pd.concat([
            matches,
            results[['db_index', 'db_candidate', 'matching_score']]
        ], axis=1)
        
        return updated_results


def find_match_block(qstart, db_path:tuple, db_candidate:tuple):
    qoffset, db_offset, size = difflib.SequenceMatcher(None, db_path, db_candidate).find_longest_match()
    
    return qstart + qoffset, qstart + qoffset + size, db_offset, db_offset + size, size
