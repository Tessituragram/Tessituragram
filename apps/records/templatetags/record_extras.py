from django import template
from apps.records.columns import COLUMN_MAP

register = template.Library()


@register.filter
def column_value(record, key):
    entry = COLUMN_MAP.get(key)
    if not entry:
        return ""
    _, _, accessor = entry
    try:
        return accessor(record)
    except Exception:
        return ""