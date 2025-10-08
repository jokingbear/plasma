import math
import numpy as np

from .base import BaseDataset


class SampleBase(BaseDataset):
    
    def sample(self, num_sample, replace=False, seed=None):
        np.random.seed(seed)
        indices = np.random.choice(num_sample, replace=replace)
        return SampledDataset(self, indices)


class SampledDataset(SampleBase):
    
    def __init__(self, original:SampleBase, indices):
        super().__init__()
        
        self.original = original
        self.indices = indices
    
    def get_item(self, idx):
        return self.original[self.indices[idx]]
    
    def get_len(self):
        return len(self.indices)
