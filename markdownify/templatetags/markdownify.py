from django import template
from django.conf import settings
import markdown
import bleach

register = template.Library()


@register.filter
def markdownify(text):
    # safe mode is deprecated, see: https://pythonhosted.org/Markdown/reference.html#safe_mode
    html = markdown.markdown(text, safe_mode=getattr(settings, 'MARKDOWNIFY_SAFEMODE', 'escape'))
    if getattr(settings, 'MARKDOWNIFY_BLEACH', True):
        html = bleach.clean(html,
                            tags=settings.MARKDOWNIFY_WHITELIST_TAGS, )
        html = bleach.linkify(html)
    return html
