# Mostly coming from
# https://emilstenstrom.github.io/justhtml/bleach-migration.html
from collections.abc import Collection, Mapping

from justhtml import UrlPolicy, UrlRule

URL_LIKE_ATTRS = {
    "href",
    "src",
    "srcset",
    "poster",
    "action",
    "formaction",
    "data",
    "cite",
    "background",
    "ping",
}

BLEACH_DEFAULT_TAGS = frozenset(
    {
        "a",
        "abbr",
        "acronym",
        "b",
        "blockquote",
        "code",
        "em",
        "i",
        "li",
        "ol",
        "strong",
        "ul",
    }
)
BLEACH_DEFAULT_ATTRIBUTES = {
    "a": {"href", "title"},
    "abbr": {"title"},
    "acronym": {"title"},
}
BLEACH_DEFAULT_PROTOCOLS = frozenset({"http", "https", "mailto"})
BLEACH_DEFAULT_CSS_PROPERTIES = frozenset(
    (
        "azimuth",
        "background-color",
        "border-bottom-color",
        "border-collapse",
        "border-color",
        "border-left-color",
        "border-right-color",
        "border-top-color",
        "clear",
        "color",
        "cursor",
        "direction",
        "display",
        "elevation",
        "float",
        "font",
        "font-family",
        "font-size",
        "font-style",
        "font-variant",
        "font-weight",
        "height",
        "letter-spacing",
        "line-height",
        "overflow",
        "pause",
        "pause-after",
        "pause-before",
        "pitch",
        "pitch-range",
        "richness",
        "speak",
        "speak-header",
        "speak-numeral",
        "speak-punctuation",
        "speech-rate",
        "stress",
        "text-align",
        "text-decoration",
        "text-indent",
        "unicode-bidi",
        "vertical-align",
        "voice-family",
        "volume",
        "white-space",
        "width",
    )
)


def build_url_policy(
    allowed_tags: Collection[str],
    allowed_attributes: Mapping[str, Collection[str]],
    protocols: Collection[str],
) -> UrlPolicy:
    rules = {}

    global_attrs = allowed_attributes.get("*", ())
    for tag in allowed_tags:
        for attr in global_attrs:
            if attr in URL_LIKE_ATTRS:
                rules[(tag, attr)] = UrlRule(
                    allowed_schemes=protocols,
                    allow_relative=True,
                )

    for tag, attrs in allowed_attributes.items():
        if tag == "*":
            continue
        for attr in attrs:
            if attr in URL_LIKE_ATTRS:
                rules[(tag, attr)] = UrlRule(
                    allowed_schemes=protocols,
                    allow_relative=True,
                )
    return UrlPolicy(allow_rules=rules)
