from typing import Sequence
from .index import Index
from .regex_tokenizer import RegexTokenizer
from .inquirer import PathInquirer
from .token_matcher import TokenMatcher
from ..data_model.collections import ZippedStream


class StreamIndex:
    
    def __init__(
            self, 
            data:Sequence[str],
            group_splitter=r'[^\.\n]+', tokenizer=r'\w+',
            token_threshold=0.7, topk=5,
        ):
        super().__init__()
        
        tokenizer = RegexTokenizer(tokenizer)
        index = Index(data, tokenizer)
        token_matcher = TokenMatcher(index, token_threshold)
        
        self._index = index
        self.context_splitter = RegexTokenizer(group_splitter)
        self.path_inquirer = PathInquirer(self._index, tokenizer, token_matcher, topk)
    
    def __call__(self, query:str):
        contexts = self.context_splitter(query)
        return (
            ZippedStream[int, int, str](contexts.itertuples(index=False))
            .unwind(lambda start, end, context:
                self.path_inquirer(context)
                .select(lambda m:m.update(start))
            )
        )

    def run(self, query:str):
        return self(query)
