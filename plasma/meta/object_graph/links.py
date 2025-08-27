from enum import Enum, auto, Flag


class Link(Flag):
    CONTAINS = auto()
    DEPEND_ON = auto()
    DELEGATE_TO = auto()
