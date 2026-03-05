from .pipe import AutoPipe
from abc import abstractmethod


class State[**I, O](AutoPipe[I, O]):

    @abstractmethod
    def release(self):
        pass
