from django import template

register = template.Library()

@register.simple_tag
def get_range(start_year, num_years):
    return range(start_year, start_year + num_years)

@register.filter
def index(indexable, i):
    return indexable[i]


