from django import template

register = template.Library()

@register.filter(name='percentage')
def percentage(value):

    return "{:0.1%}".format(value)
