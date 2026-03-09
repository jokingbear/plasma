from .base2 import MODEL_FLAG
from ...functional import ReadableClass


class ModelInquirer(ReadableClass):
    
    def __init__(self, cls:type):
        self.cls = cls
    
    def is_data_model(self):
        return hasattr(self.cls, MODEL_FLAG)
    
    def fields(self):
        return self.cls.__annotations__
