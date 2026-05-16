import numpy as np

from dataclasses import dataclass
from scipy.stats import hmean
from typing import Any, Sequence, Self, Iterable
from rich.tree import Tree
from .utils import format_score
from ..tree_rep import tree_repr
from ....utils import Formatter


@tree_repr
@dataclass(repr=False)
class StandardTrace:
    target:Any
    ref:Any
    score:float
    
    def _tree(self, tree:Tree):
        tree.add(Formatter.BLUE(f'target={self.target}'))
        tree.add(Formatter.GREEN(f'ref={self.ref}'))
        tree.add(format_score(f'score={self.score:.04f}', self.score))
        return tree


@tree_repr
@dataclass(repr=False)
class SummaryTrace:
    score:float
    items:Sequence[StandardTrace|Self]
    
    def _tree(self, tree:Tree):
        tree.add(f'score={self.score:.04f}')
        
        items = tree.add('items')
        for i in self.items:
            i._tree(items)
        
        return tree


@tree_repr
class Summary:
    
    def __init__(self, num_target, num_refs, traces:dict[str, StandardTrace|SummaryTrace]):
        precisions = [max(t.score, 0.1) for t in traces.values()]
        precisions.extend([0.1] * (num_target - len(traces)))

        precision = hmean(precisions)
        recall = sum([t.score for t in traces.values()], 0) / num_refs
        score = hmean([precision, recall])
        
        self.precision = precision
        self.recall = recall
        self.score = score
        self.traces = traces
    
    def _tree(self, tree:Tree):        
        tree.add(f'score={self.score:.04f}')
        tree.add(f'precision={self.precision:.04f}')
        tree.add(f'recall={self.recall:.04f}')
        
        traces = tree.add('traces')
        for k, v in sorted(self.traces.items(), key=lambda kv:kv[0]):
            metric = f'{k}={v.score:.04f}'
            if v.score < 0.5:
                metric = Formatter.RED(metric)
            elif v.score < 0.9:
                metric = Formatter.YELLOW(metric)

            traces.add(metric)
        
        return tree


@tree_repr
@dataclass
class KeyTrace[T, R]:
    target_key:T
    ref_key:R
    trace:StandardTrace|SummaryTrace

    def _tree(self, tree:Tree):
        tree.add(Formatter.BLUE(f'target={self.target_key}'))
        tree.add(Formatter.GREEN(f'ref={self.ref_key}'))
        self.trace._tree(tree.add('trace='))
        
        return tree


@tree_repr
class FieldSummary:
    
    def __init__(self, name:str, traces:Sequence[KeyTrace]):
        self.name = name
        self.traces = traces
        self.score = float(np.mean([t.trace.score for t in traces])) 
    
    def _tree(self, tree:Tree):
        tree = Tree(self.name)
        tree.add(f'score={self.score:.04f}')
        
        traces = tree.add('traces')
        for t in sorted(self.traces, key=lambda t: t.trace.score)[:5]:
            t._tree(traces)

        if len(self.traces) > 5:
            traces.add('...')
        
        return tree


@tree_repr
class BatchSummary:
    
    def __init__(self, fields:Iterable[tuple[str, Sequence[KeyTrace]]]):
        field_dict = dict(fields)

        self.scores = {
            f: float(np.mean([t.trace.score for t in traces])) 
            for f, traces in field_dict.items()
        }
        self.fields = {f: FieldSummary(f, traces) for f, traces in field_dict.items()}
    
    def _tree(self, tree:Tree):
        overall = hmean([*self.scores.values()])
        tree.add(f'overall_score={overall:.04f}')
        
        details = tree.add('fields')
        for field, score in sorted(self.scores.items(), key=lambda fs: fs[1]):
            details.add(format_score(f'{field}: {score:.4f}', score))
            
        return tree
