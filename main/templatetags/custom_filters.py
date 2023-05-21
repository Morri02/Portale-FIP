from django import template

register = template.Library()


@register.filter(name='range')
def range(value):
    return range(value)
