import traceback


class TraceableException(Exception):
    
    def __init__(self, *args, exception:Exception=None):
        exception_args = [] if exception is None else exception.args
        super().__init__(*args, *exception_args)
        
        self.info = traceback.format_exc()
