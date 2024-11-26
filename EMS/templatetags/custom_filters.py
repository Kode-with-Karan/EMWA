# custom_filters.py
from django import template

register = template.Library()

@register.filter
def replace_slash(value):
    """Replaces all '/' with '-' in a string."""
    return value.replace('/', '$$@$$')

@register.filter
def short10(value):
    """Replaces all '/' with '-' in a string."""
    return value[0:10]+"..."

@register.filter
def desc_shorter(value):
    if(value.__len__() < 80):
        return value[0:20]
    else:
        return value[0:80]+"..."

@register.filter
def name_shorter(value):
    if(value.__len__() < 15):
        return value[0:15]
    else:
        return value[0:15]+"..."
    
@register.filter
def checkHttp(value):
    return "https://"+(value.split("https://")[-1])