import math
import numpy as np

from .base import BaseDataset


class SampleBase[T](BaseDataset[T]):
    
    def sample(self, num_sample, replace=False, seed=None):
        np.random.seed(seed)
        indices = np.random.choice(len(self), replace=replace, size=num_sample)
        return SampledDataset(self, indices)


class SampledDataset[T](SampleBase[T]):
    
    def __init__(self, original:SampleBase[T], indices):
        super().__init__()
        
        self.original = original
        self.indices = indices
    
    def get_item(self, idx):
        idx = self.indices[idx]
        return self.original[idx]
    
    def get_len(self):
        return len(self.indices)
