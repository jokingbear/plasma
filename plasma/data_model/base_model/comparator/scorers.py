from difflib import SequenceMatcher


def score_generic(target, ref):
    return target == ref


def score_str(target, ref):
    return SequenceMatcher(None, target.lower(), ref.lower()).ratio()
