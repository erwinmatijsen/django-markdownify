from collections.abc import Iterable
import re

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

import markdown
from justhtml import JustHTML, Linkify, SanitizationPolicy

from markdownify import bleach_compat


register = template.Library()


@register.filter
def markdownify(text, custom_settings="default"):

    try:
        markdownify_settings = settings.MARKDOWNIFY[custom_settings]
    except (AttributeError, KeyError):
        markdownify_settings = {}

    # Bleach settings
    whitelist_tags = markdownify_settings.get('WHITELIST_TAGS', bleach_compat.BLEACH_DEFAULT_TAGS)
    whitelist_attrs = markdownify_settings.get('WHITELIST_ATTRS', bleach_compat.BLEACH_DEFAULT_ATTRIBUTES)
    whitelist_styles = markdownify_settings.get('WHITELIST_STYLES', bleach_compat.BLEACH_DEFAULT_CSS_PROPERTIES)
    whitelist_protocols = markdownify_settings.get('WHITELIST_PROTOCOLS', bleach_compat.BLEACH_DEFAULT_PROTOCOLS)

    # Markdown settings
    strip = markdownify_settings.get('STRIP', True)
    extensions = markdownify_settings.get('MARKDOWN_EXTENSIONS', [])
    extension_configs = markdownify_settings.get('MARKDOWN_EXTENSION_CONFIGS', {})

    # Linkify
    linkify_text = markdownify_settings.get('LINKIFY_TEXT', {"PARSE_URLS": True})
    transforms = []
    if linkify_text.get("PARSE_URLS"):
        transforms.append(Linkify(skip_tags=linkify_text.get('SKIP_TAGS', [])))
    else:
        transforms.append(Linkify(enabled=False))
    transforms.extend(linkify_text.get('TRANSFORMS', []))

    # Convert markdown to html
    html = markdown.markdown(text or "", extensions=extensions, extension_configs=extension_configs)

    # Sanitize html if wanted
    sanitization_kwargs = {
        "sanitize": True,
        "policy": None,
    }
    if markdownify_settings.get("BLEACH", True):
        if isinstance(whitelist_attrs, dict):
            attrs = {tag: set(values) for tag, values in whitelist_attrs.items()}
        elif isinstance(whitelist_attrs, Iterable):
            attrs = {"*": set(whitelist_attrs)}
        elif callable(whitelist_attrs):
            raise TypeError("Using a callback for filtering attributes is not supported by JustHTML.")
        else:
            raise TypeError(type(whitelist_attrs))
        if strip:
            disallowed_tag_handling = "unwrap"
        else:
            disallowed_tag_handling = "escape"
            # Bleach defaults to strip_comments=True. If you use escape mode
            # (`strip=False`) and still want comments removed rather than displayed,
            # remove comments before parsing.
            html = re.sub(r"<!--.*?-->", "", html, flags=re.DOTALL)
        sanitization_kwargs["policy"] = SanitizationPolicy(
            allowed_tags=whitelist_tags,
            allowed_attributes=attrs,
            allowed_css_properties=whitelist_styles,
            url_policy=bleach_compat.build_url_policy(whitelist_tags, attrs, whitelist_protocols),
            disallowed_tag_handling=disallowed_tag_handling,
        )
    else:
        sanitization_kwargs["sanitize"] = False
    html = JustHTML(html, fragment=True, transforms=transforms, **sanitization_kwargs).to_html(pretty=False)
    return mark_safe(html)


def do_markdownify(parser, token):
    # Set up the nodelist and parse till we hit the endmarkdownify block
    nodelist = parser.parse(("endmarkdownify",))
    parser.delete_first_token()

    # Get the settings from the tag
    try:
        markdownify_settings = token.split_contents()[1]
    except IndexError:
        markdownify_settings = "default"

    return MarkDownifyNode(nodelist, markdownify_settings)


class MarkDownifyNode(template.Node):
    def __init__(self, nodelist, markdownify_settings):
        self.nodelist = nodelist
        self.markdownify_settings = markdownify_settings

    def render(self, context):

        # Build new nodelist with rendered and markdownified nodes
        node_list = []
        for node in self.nodelist:
            md_node = markdownify(node.render(context), custom_settings=self.markdownify_settings)
            node_list.append(md_node)

        return "".join(node_list)


register.tag("markdownify", do_markdownify)
