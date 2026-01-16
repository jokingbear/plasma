from .data_model import Form
from .factory import READER_FACTORY

@READER_FACTORY.register(Form.field2, Form.field5.field1)
class Reader2:...
