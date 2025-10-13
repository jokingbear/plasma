import pandas as pd

from .sample import SampleBase


class DynamicDataset[V, T](SampleBase[T]):

    def __init__(self, data:list[V]) -> None:
        super().__init__()

        self._data = data
    
    def get_len(self):
        return len(self._data)
    
    def get_item(self, idx):
        item = self.pick_item(idx)
        return self.process_item(item)
    
    def pick_item(self, idx):
        data = self._data
        if isinstance(data, (pd.DataFrame, pd.Series)):
            return data.iloc[idx]
        else:
            return data[idx]

    def process_item(self, item:V) -> T:...
