from .publisher import PubZMQ
from ....serializers import Serializer, Pickler
from ....functional import ReadableClass


class ShardPublisherQueue(ReadableClass):
    
    def __init__(self, 
            *connections:str,
            timeout:float=1,
            serializer:Serializer=Pickler(),
        ):
        pass
    