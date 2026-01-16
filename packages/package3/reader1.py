from .data_model import Form
from .factory import READER_FACTORY

@READER_FACTORY.register(Form.field1)
class Reader1:...