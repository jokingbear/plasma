import pandas as pd
import itertools

from typing import Callable

from .matcher import SegmentMatch
from .solver import Solver
from .position_graph import PositionGraph
from .refiner import SegmentRefiner, PathRefiner
from .segment import Match, Segment
from ..index import Index
from ...functional import ReadableClass
from ...data_model.collections import Stream


class PathInquirer(ReadableClass):
    
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
        self._segment2match = SegmentMatch()
    
    def __call__(self, query:str):
        query = query.lower()
        qtoken_frame = self.tokenizer(query)
        qtoken_2_dbtokens = self.token_matcher(qtoken_frame['token'].unique().tolist())
        position_graph = PositionGraph(self.index, qtoken_frame, qtoken_2_dbtokens)
        
        paths = [*position_graph.generate_paths()]
        if len(paths) > 0:
            paths = self._path_refiner(paths)

        segments = list[Segment]()
        solver = Solver(position_graph, self.index.get_path_args)
        for position_path in paths:
            segments.extend(solver(position_path))

        if len(segments) > 0:
            segments = self._segment_refiner(segments)
            return (
                Stream(segments)
                .groupby(lambda s: (s.qtoken_start, s.qtoken_end), lambda s:s)
                .map_value(lambda _, gs: 
                    Stream(gs)
                    .unwind(lambda s:self._segment2match(s, qtoken_frame, self.index))
                    .sort(
                        lambda m:(m.matching_score, m.matched_len, m.coverage_score), 
                        reverse=True
                    )
                    .take(self.topk)
                )
                .unwind(lambda _, ms: ms)
            )

        return Stream[Match]([])
