import difflib

from .index import Index
from ..data_model.collections import Stream, ZippedStream


class TokenMatcher:

    def __init__(self, index:Index, threshold:float, topk:int|None):
        super().__init__()

        self._index = index
        self.threshold = threshold
        self.topk = topk
        self.scorer = _compute_score
    
    def __call__(self, tokens:list[str]):
        return dict(
            Stream(tokens).product(self._index.tokens)
            .groupby(
                lambda qtk, _: qtk, 
                lambda qtk, rtk: (rtk, self.scorer(qtk, rtk))
            ).map_value(lambda _, ms: 
                ZippedStream(ms)
                .filter(lambda _, s: s >= self.threshold)
                .sort(lambda _, s: s, reverse=True)
            ).select(lambda _, ms: 
                {qtk: score for qtk, score in ms[:self.topk]}
            )
        )


def _compute_score(s1:str, s2:str):
    return difflib.SequenceMatcher(None, s1, s2).ratio()
