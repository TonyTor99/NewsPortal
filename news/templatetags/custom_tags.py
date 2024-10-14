from django import template
from datetime import datetime

register = template.Library()


@register.simple_tag()
def time_now(format_string='%Y %b %d'):
    return datetime.utcnow().strftime(format_string)


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()
