import traceback


class TraceableException(Exception):
    
    def __init__(self, exception:Exception, *args):
        super().__init__(*exception.args, *args)
        
        self.info = traceback.format_exc()
