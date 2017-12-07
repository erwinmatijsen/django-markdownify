from django import template
from django.conf import settings
import markdown
import bleach
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def markdownify(text):

    # Get the settings or set defaults if not set
    whitelist_tags = getattr(settings, 'MARKDOWNIFY_WHITELIST_TAGS', bleach.sanitizer.ALLOWED_TAGS)
    whitelist_attrs = getattr(settings, 'MARKDOWNIFY_WHITELIST_ATTRS', bleach.sanitizer.ALLOWED_ATTRIBUTES)
    whitelist_styles = getattr(settings, 'MARKDOWNIFY_WHITELIST_STYLES', bleach.sanitizer.ALLOWED_STYLES)
    whitelist_protocols = getattr(settings, 'MARKDOWNIFY_WHITELIST_PROTOCOLS', bleach.sanitizer.ALLOWED_PROTOCOLS)
    strip = getattr(settings, 'MARKDOWNIFY_STRIP', True)
    extensions = getattr(settings, 'MARKDOWNIFY_MARKDOWN_EXTENSIONS', [])

    # Convert markdown to html
    html = markdown.markdown(text, extensions=extensions)

    # Sanitize html if wanted
    if getattr(settings, 'MARKDOWNIFY_BLEACH', True):
        html = bleach.clean(html,
                            tags=whitelist_tags,
                            attributes=whitelist_attrs,
                            styles=whitelist_styles,
                            protocols=whitelist_protocols,
                            strip=strip,)

        html = bleach.linkify(html)

    return mark_safe(html)

