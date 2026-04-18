import difflib
import numpy as np
import networkx as nx
import pandas as pd

from scipy.stats import hmean
from .segment import Match
from .position_path import PositionPath
from .segment import Segment
from ..index import Index
from ...data_model.collections import Stream, product_range


class SegmentMatch:
    
    def __call__(self, s:Segment, qtoken_frame:pd.DataFrame, index:Index): 
        for a in s.db_path_args:
            db_path = index.get_path(a)
            match = _match(s.position_path, db_path)
            if match is None:
                continue

            yield _construct(s.position_path, a, match, qtoken_frame, index)


def _match(position_path:PositionPath, db_path:tuple[str]):
    m = len(position_path)
    n = len(db_path)
    
    matching_matrix = np.zeros([m, n], dtype=int)
    for i, j in product_range(m, n):
        matching_matrix[i, j] = position_path[i][1] == db_path[j]
            
    graph = nx.Graph()
    graph.add_nodes_from(ij for ij in product_range(m, n) if matching_matrix[*ij] == 1)
    for i, j in product_range(m - 1, n - 1):
        if matching_matrix[i, j] == matching_matrix[i + 1, j + 1] == 1:
            graph.add_edge((i, j), (i + 1, j + 1))

    matches = (
        Stream[set[tuple[int, int]]](nx.connected_components(graph))
        .groupby(len, min)
        .select(lambda kv: (kv[0], min(kv[1])))
    )

    if matches.empty:
        return
    
    size, offsets = max(matches)
    return difflib.Match(*offsets, size)


def _construct(
        position_path:PositionPath, 
        db_path_arg:int, 
        match:difflib.Match,
        qtoken_frame:pd.DataFrame, 
        index:Index
    ):
    db_path = index.get_path(db_path_arg)
    coverage_score = match.size / len(db_path)
    
    db_char_start, _ = index.get_char_interval(db_path_arg, match.b)
    _, db_char_end = index.get_char_interval(db_path_arg, match.b + match.size - 1)
    score = hmean([position_path.score(a) for a in range(match.a, match.a + match.size)])
    return Match(
        qtoken_frame.iloc[position_path.offset(match.a)]['start_idx'], 
        qtoken_frame.iloc[position_path.offset(match.a + match.size - 1)]['end_idx'],
        db_path_arg,
        db_char_start,
        db_char_end,
        index.get_data(db_path_arg),
        score, coverage_score, match.size,
        hmean([score, coverage_score])
    )
