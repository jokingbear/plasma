from enum import Flag, auto


class Node(Flag):
    CONTEXT = auto()
    INITATOR = auto()
    SINGLETON = auto()
    LEAF = auto()
    FACTORY = auto()
