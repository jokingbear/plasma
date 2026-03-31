from typing import Iterable

from ..communicators import AsyncFlow
from ..communicators.accumulators import DynamicAccumulator


class Flow[O](AsyncFlow):
    accumulator:DynamicAccumulator[object, Iterable[O]]
