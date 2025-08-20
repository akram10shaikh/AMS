from django import template

register = template.Library()
@register.filter
def dict_get(dictionary, key):
    """Returns the value from a dictionary for the given key."""
    return dictionary.get(key, "")
