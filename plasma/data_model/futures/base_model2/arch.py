SCHEMA_FIELD = '__schema'
ITEM_PREFIX = '@'
MODEL_FIELD = '__MODEL'


def is_model(t:type):
    return hasattr(t, SCHEMA_FIELD)
