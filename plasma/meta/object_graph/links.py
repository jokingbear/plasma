from enum import Enum, auto, Flag


class Link(Flag):
    CONTAINS = 0
    DEPEND_ON = 1
    DELEGATE_TO = 2
