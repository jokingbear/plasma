SCHEMA_FIELD = '__schema'
ITEM_PREFIX = '@'


def is_model(t:type):
    return hasattr(t, SCHEMA_FIELD)
