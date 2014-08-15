__author__ = 'kevin'
from django import template

register = template.Library()

@register.filter
def is_full(value, arg):
    for item in arg:
        if value==item:
            return "booked"

@register.filter
def custom_add(value,arg):
    return value+'-'+str(arg)