import numpy as np

from ...functional import AutoPipe
from .segment import Segment, Match
from collections import defaultdict


class SegmentRefiner(AutoPipe[[list[Segment]], list[Segment]]):
    
    def run(self, segments:list[Segment]):
        interval_counts = defaultdict(lambda: 0)
        intervals = []
        for s in segments:
            interval_counts[s.token_start, s.token_end] += 1
            intervals.append([s.token_start, s.token_end])
        
        intervals = np.array(intervals)
        bounds = (intervals[:, 0] <= intervals[:, [0]]) & (intervals[:, [1]] <= intervals[:, 1])
        bound_counts = bounds.sum(axis=1)
        limits = np.array([interval_counts[s, e] for s, e in intervals])
        unbound_args, = np.where(bound_counts == limits)

        return [segments[a] for a in unbound_args]



class MatchRefiner(AutoPipe[[list[Match]], list[Match]]):
    
    def run(self, matches:list[Match]):
        interval_counts = defaultdict(lambda: 0)
        intervals = []
        for s in matches:
            interval_counts[s.qchar_start, s.qchar_end] += 1
            intervals.append([s.qchar_start, s.qchar_end])
        
        intervals = np.array(intervals)
        bounds = (intervals[:, 0] <= intervals[:, [0]]) & (intervals[:, [1]] <= intervals[:, 1])
        bound_counts = bounds.sum(axis=1)
        limits = np.array([interval_counts[s, e] for s, e in intervals])
        unbound_args, = np.where(bound_counts == limits)

        return [matches[a] for a in unbound_args]
