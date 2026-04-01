from ..communicators import AsyncFlow
from ..communicators.accumulators import DynamicAccumulator


class Flow(AsyncFlow):
    accumulator:DynamicAccumulator
