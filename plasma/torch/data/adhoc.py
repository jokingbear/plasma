import pandas as pd

from .sample import SampleBase
from typing import Callable


class AdhocData[V, T](SampleBase[T]):

    def __init__(self, arr:list[V], mapping:Callable[[V], T], kwargs:dict=None):
        super().__init__()

        self.source = arr
        self.mapping = mapping
        self.kwargs = kwargs or {}

    def get_len(self):
        return len(self.source)

    def get_item(self, idx):
        if isinstance(self.source, (pd.DataFrame, pd.Series)):
            item = self.source.iloc[idx]
        else:
            item = self.source[idx]

        return self.mapping(item, **self.kwargs)
