from django import template
from django.template.defaultfilters import stringfilter
from codetalker.parser import Shortcode_Parser

register = template.Library()
codetalker = Shortcode_Parser()


@register.filter
@stringfilter
def expand_shortcodes(val):
    return codetalker.expand_shortcodes(val)
