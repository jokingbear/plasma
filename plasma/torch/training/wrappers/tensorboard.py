import torch.nn as nn
import torch.optim as optimizers

from torch.utils.tensorboard import SummaryWriter
from ..bases import ForwardWrapper
from typing import Callable


class Tensorboard(ForwardWrapper):

    def __init__(self, log_dir, n=1, 
                logger:Callable[[object, optimizers.lr_scheduler.LRScheduler], dict[str, float]]=None
            ):
        super().__init__()

        self.log_dir = log_dir
        self._writer = SummaryWriter(self.log_dir)
        self._counter = 0
        self.n = n
        self.log_func = logger or log

    def append(self, trainer, i, inputs, outputs):
        if trainer.rank == 0 and outputs is not None:
            writer = self._writer
            infos = self.log_func(outputs, trainer.scheduler)
            
            for key, value in infos.items():
                writer.add_scalar(key, value, self._counter)
        
        self._counter += 1


def log(outputs, scheduler:optimizers.lr_scheduler.LRScheduler) -> dict[str, float]:
    infos = {'loss': outputs.float()}
    
    if scheduler is not None:
        for i, l in enumerate(scheduler.get_last_lr()):
            infos[f'lr-{i}'] = l

    return infos
