import pandas as pd
import itertools

from typing import Callable

from .solver import Solver
from .position_graph import PositionGraph
from .refiner import SegmentRefiner, PathRefiner
from .segment import Match, Segment
from ..index import Index
from ...functional import AutoPipe
from ...data_model.collections import groupby, Stream


class PathInquirer(AutoPipe[[str], Stream[Match]]):
    
    def __init__(self, 
                index:Index, 
                tokenizer:Callable[[str], pd.DataFrame],
                token_matcher:Callable[[list[str]], dict[str, dict[str, float]]],
                topk:int,
            ):
        super().__init__()
        
        self.index = index
        self.tokenizer = tokenizer
        self.token_matcher = token_matcher
        self.topk = topk
        self._path_refiner = PathRefiner()
        self._segment_refiner = SegmentRefiner()
    
    def run(self, query:str):
        query = query.lower()
        qtoken_frame = self.tokenizer(query)
        qtoken_2_dbtokens = self.token_matcher(qtoken_frame['token'].unique())
        position_graph = PositionGraph(self.index, qtoken_frame, qtoken_2_dbtokens)
        
        paths = [*position_graph.generate_paths()]
        if len(paths) > 0:
            paths = self._path_refiner(paths)

        segments = list[Segment]()
        solver = Solver(position_graph, self.index.get_path_args)
        for position_path in paths:
            segments.extend(solver(position_path))

        matches = list[Match]()
        if len(segments) > 0:
            segments = self._segment_refiner(segments)
            grouped_segments = groupby[tuple, Segment](segments, key=lambda s: (s.token_start, s.token_end))
            for _, gsegments in grouped_segments.items():                
                matched_paths:list[Match] = []
                for s in gsegments:
                    matched_paths.extend(s.get_matches(qtoken_frame, self.index))
                matched_paths = sorted(matched_paths, key=lambda p:(p.matching_score, p.matched_len, p.coverage_score), reverse=True)
                matches.extend(matched_paths[:self.topk])
        
        return Stream(matches)
