import itertools

from scipy.stats import hmean
from typing import Any, Callable, Sequence
from .traces import StandardTrace, SummaryTrace, Summary
from ..utils import is_data_model
from ..schemas import schema as schema_getter
from ...collections import Stream, ZippedStream

Scorer = Callable[[Any, Any], float|bool]


class Comparator:
    
    def __init__(self):
        self._sub_comparators = dict[tuple, Scorer]()
        self._primitive_comparators = dict[type, Scorer]()
    
    def __call__(self, target:Any, ref:Any):
        assert is_data_model(target)
        assert is_data_model(ref)
        assert type(target) is type(ref)
        
        schema = schema_getter(target)
        target_realization = schema.realize(target)
        target_endpoints = [*target_realization.endpoints]
        
        ref_realization = schema.realize(ref)
        ref_endpoints = [*ref_realization.endpoints]
        shared_fields = set(target_endpoints).intersection(ref_endpoints)
        
        traces = dict(
            Stream(shared_fields)
            .split(lambda n: 
                (n, target_realization.value(n), ref_realization.value(n))
            )
            .select(lambda n, t, r: (n, self._compute_score(t, r)))
            .groupby(lambda n,_: schema.real_to_rep(n), lambda _,t:t)
            .map_key(lambda n: '.'.join(str(a) for a in n))
            .select(lambda _, traces:self._combine_trace(traces))
        )
        return Summary(len(target_endpoints), len(ref_endpoints), traces)
    
    def _compute_score(self, target, ref):
        if type(target) is not type(ref):
            return StandardTrace(target, ref, 0)

        if isinstance(target, Sequence):
            item_traces = (
                ZippedStream(itertools.zip_longest(target, ref))
                .project(lambda t, r: self._compute_score(t, r))
                .evaluate()
            )
            
            precision = hmean([max(t.score, 0.1) for t in item_traces[:len(target)]])
            recall = sum([t.score for t in item_traces[:len(ref)]], 0) / len(ref)
            return SummaryTrace(
                hmean([precision, recall]),
                item_traces
            )
        
        assert type(target) in self._primitive_comparators, f'unrecognized type {type(target)}'
        return StandardTrace(
            target, ref,
            float(self._primitive_comparators[type(target)](target, ref))
        ) 

    def _combine_trace(self, traces:Sequence[StandardTrace|SummaryTrace]):
        if len(traces) == 0:
            return traces[0]
        else:
            return SummaryTrace(
                hmean([t.score for t in traces]),
                traces
            )
