from django import template

register = template.Library()

@register.filter
def underscore_to_space(value):
    if isinstance(value, str):
        return value.replace('_', ' ')
    return value

@register.filter
def get_item(dictionary, key):
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None