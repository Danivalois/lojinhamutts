# templatetags/mutts_filters.py
from django import template

register = template.Library()

@register.filter(name='replace')
def replace(value, arg):
    """Replaces all occurrences of the first argument with the second argument string"""
    return str(value).replace(arg.split(',')[0], arg.split(',')[1])