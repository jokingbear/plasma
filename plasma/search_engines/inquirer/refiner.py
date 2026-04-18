import numpy as np
import itertools

from collections import defaultdict, Counter
from .position_path import PositionPath
from .segment import Segment, Match
from ...functional import AutoPipe


class SegmentRefiner(AutoPipe[[list[Segment]], list[Segment]]):
    
    def run(self, segments:list[Segment]):
        unique_segments = dict[tuple, Segment]()
        for s in segments:
            key = tuple(s.position_path)
            if key not in unique_segments:
                unique_segments[key] = s

        interval_counts = Counter()
        intervals = list[list]()
        segments = []
        for s in unique_segments.values():
            interval_counts[s.qtoken_start, s.qtoken_end] += 1
            intervals.append([s.qtoken_start, s.qtoken_end])
            segments.append(s)
        
        intervals = np.array(intervals)
        bounds = (intervals[:, 0] <= intervals[:, [0]]) & (intervals[:, [1]] <= intervals[:, 1])
        bound_counts = bounds.sum(axis=1)
        limits = np.array([interval_counts[s, e] for s, e in intervals])
        unbound_args, = np.where(bound_counts == limits)

        return [segments[a] for a in unbound_args]


class PathRefiner(AutoPipe[[list[PositionPath]], list[PositionPath]]):
    
    def run(self, data:list[PositionPath]):
        interval_counts = Counter()
        intervals = []
        for p in data:
            interval_counts[p.offset(0), p.offset(-1)] += 1
            intervals.append([p.offset(0), p.offset(-1)])
        
        intervals = np.array(intervals)
        bounds = (intervals[:, 0] <= intervals[:, [0]]) & (intervals[:, [1]] <= intervals[:, 1])
        bound_counts = bounds.sum(axis=1)
        limits = np.array([interval_counts[s, e] for s, e in intervals])
        unbound_args, = np.where(bound_counts == limits)

        return [data[a] for a in unbound_args]
