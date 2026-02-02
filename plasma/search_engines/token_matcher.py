import difflib

from ..functional import AutoPipe
from collections import defaultdict
from .index import Index


class TokenMatcher(AutoPipe[[list[str]], dict[str, dict[str, float]]]):

    def __init__(self, index:Index, threshold:float):
        super().__init__()

        self._index = index
        self.threshold = threshold
    
    def run(self, tokens:list[str]):
        matches = defaultdict(lambda: {})
        for qtk in tokens:
            for db_tk in self._index.tokens:
                score = difflib.SequenceMatcher(None, qtk, db_tk).ratio()
                if score >= self.threshold:
                    matches[qtk][db_tk] = score

        return matches
