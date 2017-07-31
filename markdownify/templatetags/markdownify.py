from django import template
from django.conf import settings
import markdown
import bleach

register = template.Library()


@register.filter
def markdownify(text):

    # Get the settings or set defaults if not set
    whitelist_tags = getattr(settings, 'MARKDOWNIFY_WHITELIST_TAGS', bleach.sanitizer.ALLOWED_TAGS)
    whitelist_attrs = getattr(settings, 'MARKDOWNIFY_WHITELIST_ATTRS', bleach.sanitizer.ALLOWED_ATTRIBUTES)
    strip = getattr(settings, 'MARKDOWNIFY_STRIP', True)

    # Convert markdown to html
    html = markdown.markdown(text)

    # Sanitize html if wanted
    if getattr(settings, 'MARKDOWNIFY_BLEACH', True):
        html = bleach.clean(html,
                            tags=whitelist_tags,
                            attributes=whitelist_attrs,
                            strip=strip, )
        html = bleach.linkify(html)

    return html
