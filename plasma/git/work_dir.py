import os

WORK_DIR = '.cache/'

def set_dir(path='.cache/'):
    if not os.path.exists(path):
        os.makedirs(path)
    
    os.environ['HF_HOME'] = path
    os.environ['TRANSFORMERS_CACHE'] = path
    
    global WORK_DIR
    WORK_DIR = path
