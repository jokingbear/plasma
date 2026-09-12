from intervaltree import Interval, IntervalTree
from .position_path import PositionPath
from .segment import Segment
from ...data_model.collections import Stream, ZippedStream


class SegmentRefiner:
    
    def __call__(self, segments:list[Segment]):
        interval_map = dict[tuple, list[Segment]]()
        for s in segments:
            p = s.position_path
            start, _ = p[0]
            if len(p) == 1:
                end = start + 1
            else:
                end, _ = p[-1]
                end += 1

            interval_map.setdefault((start, end), []).append(s)

        return _remove_contained(interval_map)


class PathRefiner:
    
    def __call__(self, data:list[PositionPath]):
        interval_map = dict[tuple, list[PositionPath]]()
        for p in data:
            start, _ = p[0]
            if len(p) == 1:
                end = start + 1
            else:
                end, _ = p[-1]
                end += 1

            interval_map.setdefault((start, end), []).append(p)

        return _remove_contained(interval_map)


def _remove_contained[T](interval_map:dict[tuple, list[T]]):
    interval_index = IntervalTree(Interval(s, e) for s, e in interval_map)
    return (
        ZippedStream[int, int](interval_map)
        .filter(lambda s, e:
            Stream[Interval](interval_index.overlap(s, e))
            .split(lambda i: (i.begin, i.end))
            .filter(
                lambda cs, ce: cs <= s and e <= ce,
                lambda cs, ce: cs != s or ce != e,
            ).empty
        ).
        unwind(lambda s, e: interval_map[s, e])
    )
