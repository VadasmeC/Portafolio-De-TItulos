from django import template

register = template.Library()

@register.filter
def range_filter(value):
    try:
        return range(int(value))
    except (TypeError, ValueError):
        return []

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


