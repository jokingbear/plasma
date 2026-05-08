import os
import torch.distributed as dist

from torch.nn.parallel import DistributedDataParallel as DDP
from ..bases import Trainer


class DistributedTrainer(Trainer):

    def __init__(
            self, 
            backend='nccl'
        ):
        super().__init__()

        rank = int(os.environ['RANK'])
        world_size = int(os.environ['WORLD_SIZE'])
        self.rank = rank
        self.world_size = world_size

        dist.init_process_group(backend)

    def __call__(self):
        super()()
        dist.destroy_process_group()
