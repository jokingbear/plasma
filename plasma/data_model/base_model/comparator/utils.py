from ....utils import Formatter


def format_score(text:str, score:float):
    if score < 0.5:
        text = Formatter.RED(text)
    elif score < 0.9:
        text = Formatter.YELLOW(text)
    
    return text
