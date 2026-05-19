from .helpers import (
    partials, chain
)
from .pipes import (
    AutoPipe, Signature, Identity,
    SequentialPipe, BaseConfigs,
    State, Wrapper, ReadableClass, Chain
) 
from . import decorators
# from .chainer import pipe
from .chainer2 import (
    pipe, auto_map, 
    partial_left, partial_right
)