from enum import Enum, auto


class Link(Enum):
    CONTAINS = 0
    DEPEND_ON = 1
    DELEGATE_TO = 2
