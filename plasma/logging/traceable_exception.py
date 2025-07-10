import traceback


class TraceableException(Exception):
    
    def __init__(self, *args, exception:Exception=None):
        exception_args = exception.args or []
        super().__init__(*args, *exception_args)
        
        self.info = traceback.format_exc()
