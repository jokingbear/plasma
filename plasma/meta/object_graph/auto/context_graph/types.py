from enum import Enum, auto


class Node(Enum):
    INITIATOR = auto()
    LEAF = auto()
    FACTORY = auto()
    SINGLETON = auto()
    DELEGATE = auto()
