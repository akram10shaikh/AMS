from django import template
register = template.Library()
@register.filter
def get_label_from_choice(choices, value):
    """
    Given a choices iterable and a value, return the display label or empty string.
    Usage: {{ AGE_CHOICES|get_label_from_choice:val }}
    """
    for v, label in choices:
        if str(v) == str(value):
            return label
    return ""

@register.filter
def dict_get(d, k):
    # For badge removal links
    return d.get(k, []) if hasattr(d, "get") else []

@register.filter
def list_without(lst, remove_value):
    "Return a list excluding remove_value."
    return [x for x in lst if x != remove_value]
