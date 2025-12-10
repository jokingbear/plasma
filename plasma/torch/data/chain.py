from .base import BaseDataset


class ChainDataset[T](BaseDataset[T]):

    def __init__(self, *datasets:BaseDataset[T]):
        super().__init__()

        self._arg2dataset = []
        self._arg2arg = []
        for d in datasets:
            self._arg2arg.extend(range(len(d)))
            self._arg2dataset.extend([d] * len(d))

        self.datasets = datasets
    
    def get_len(self):
        return len(self._arg2arg)
    
    def get_item(self, idx):
        dataset = self._arg2dataset[idx]
        dataset_arg = self._arg2arg[idx]
        return dataset[dataset_arg]
