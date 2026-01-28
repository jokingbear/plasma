import pandas as pd
import difflib

from ...functional import ReadableClass
from scipy.stats import hmean
from typing import NamedTuple, Callable
from ..index import Index
from .position_path import PositionPath


class Segment(ReadableClass):
    
    def __init__(self, position_path:PositionPath, scores:dict[object, float], db_path_args):
        super().__init__()
        
        start = position_path.offset(0)
        self.token_start = start
        self.token_end = start + len(position_path)
        self.score = hmean([scores[n] for n in position_path])
        self.db_path_args = db_path_args
        self.position_path = position_path

    def get_matches(self, qtoken_frame:pd.DataFrame, index:Index):
        for a in self.db_path_args:
            yield Match.construct(a, self, qtoken_frame, index)


class Match(NamedTuple):
    qchar_start:int
    qchar_end:int
    
    db_arg:int
    db_char_start:int
    db_char_end:int
    db_value:str
    
    matching_score:float
    coverage_score:float
    matched_len:int
    harmonic_score:float
    
    @property
    def harmonic_score(self):
        return hmean([self.matching_score, self.coverage_score])
    
    @staticmethod
    def construct(path_arg, s:Segment, 
                  qtoken_frame:pd.DataFrame, index:Index):
        standardized_qpath = tuple(tk for _, tk in s.position_path)
        db_path = index.get_path(path_arg)
        
        match = difflib.SequenceMatcher(None, standardized_qpath, db_path).find_longest_match()
        coverage_score = match.size / len(db_path)
        
        db_char_start, _ = index.get_char_interval(db_path[match.b], path_arg, match.b)
        _, db_char_end = index.get_char_interval(db_path[match.b + match.size - 1], path_arg, match.b + match.size - 1)
        
        return Match(
            qtoken_frame.iloc[s.token_start + match.a]['start_idx'], 
            qtoken_frame.iloc[s.token_start + match.a + match.size - 1]['end_idx'],
            path_arg,
            db_char_start,
            db_char_end,
            index.get_data(path_arg),
            s.score, coverage_score, match.size,
            hmean([s.score, coverage_score])
        )
