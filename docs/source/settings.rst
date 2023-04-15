Settings
========

You can change the behavior of Markdownify by adding them to your ``settings.py``. All settings are optional and will
fall back to default behavior if not specified.

.. warning:: The settings described here are for version 0.9 and up. The old style settings are deprecated and will be removed in an upcoming release. For reference, you can find the deprecated settings here: :ref:`oldsettings`

Setup
-----
Define a dictionary ``MARKDOWNIFY`` in your ``settings.py`` with one or more keys::

    MARKDOWNIFY = {
        "default": {
            ...
        },

        "other": {
            ...
        }
    }


The keys can be used in the markdownify template filter to choose which settings to use. If you define a ``default`` key, you don't have to specify it in the filter.::

    # page1.html
    {{ markdowntext|markdownify }} <!-- uses the default key -->

    # page2.html
    {{ markdowntext|markdownify:"other" }} <!-- uses the 'other' settings -->


If you don't defina a ``MARKDOWNIFY`` dict at all, all settings will fall back to defaults as described below.


Whitelist tags
--------------
Add whitelisted tags with the ``WHITELIST_TAGS`` key and a list of tags as the value.
For example::

    MARKDOWNIFY = {
        "default": {
            "WHITELIST_TAGS": [
                'a',
                'abbr',
                'acronym',
                'b',
                'blockquote',
                'em',
                'i',
                'li',
                'ol',
                'p',
                'strong',
                'ul'
            ]
        }
    }



``WHITELIST_TAGS`` defaults to `bleach.sanitizer.ALLOWED_TAGS <https://bleach.readthedocs.io/en/latest/clean.html#allowed-tags-tags>`_

Whitelist attributes
--------------------
Add whitelisted attributes with the ``WHITELIST_ATTRS`` key and a list of attributes as the value.
For example::

    MARKDOWNIFY = {
        "default": {
            "WHITELIST_ATTRS": [
                'href',
                'src',
                'alt',
            ]
        }
    }


``WHITELIST_ATTRS`` defaults to `bleach.sanitizer.ALLOWED_ATTRIBUTES <https://bleach.readthedocs.io/en/latest/clean.html#allowed-attributes-attributes>`_

Whitelist styles
----------------
Add whitelisted styles with the ``WHITELIST_STYLES`` key and a list of styles as the value.
For example::

    MARKDOWNIFY = {
        "default": {
            "WHITELIST_STYLES": [
                'color',
                'font-weight',
            ]
        }
    }

``WHITELIST_STYLES`` defaults to `bleach.css_sanitizer.ALLOWED_CSS_PROPERTIES <https://bleach.readthedocs.io/en/latest/clean.html#sanitizing-css>`_

Whitelist protocols
-------------------
Add whitelisted protocols with the ``WHITELIST_PROTOCOLS`` key and a list of protocols as the value.
For example::

    MARKDOWNIFY = {
        "default": {
            "WHITELIST_PROTOCOLS": [
                'http',
                'https',
            ]
        }
    }

``MARKDOWNIFY_WHITELIST_PROTOCOLS`` defaults to `bleach.sanitizer.ALLOWED_PROTOCOLS <https://bleach.readthedocs.io/en/latest/clean.html#allowed-protocols-protocols>`_


Enable Markdown Extensions
--------------------------
`Python-Markdown <https://python-markdown.github.io/>`_ is extensible with extensions. To enable one or more extensions,
add extensions with the ``MARKDOWN_EXTENSIONS`` key and a list of extensions as the value.
For example::

    MARKDOWNIFY = {
        "default": {
            "MARKDOWN_EXTENSIONS": [
                "markdown.extensions.fenced_code", # dotted path
                "fenced_code",  # also works
            ]
        }
    }

To pass configuration options to the extensions, define a ``MARKDOWN_EXTENSION_CONFIGS`` key in your settings.
For example::

    MARKDOWNIFY = {
        "default": {
            "MARKDOWN_EXTENSION_CONFIGS": {
                "fenced_code": {
                    "lang_prefix": "example-"
                }
            }
        }
    }

NB: It is import to use the same name in the extensions list and the configuration dict. So use ``fenced_code`` in
both places, or use ``markdown.extensions.extra.fenced_code`` in both places, but don't mix them.

``MARKDOWN_EXTENSIONS`` defaults to an empty list (so no extensions are used).
To read more about extensions and see the list of official supported extensions,
and how to configure them, go to `the markdown documentation <https://python-markdown.github.io/extensions/>`_.


Strip markup
------------
Choose if you want to `strip or escape <http://pythonhosted.org/bleach/clean.html#stripping-markup-strip>`_ tags that aren't allowed.
``STRIP: True`` (default) strips the tags.
``STRIP: False`` escapes them.::

    MARKDOWNIFY = {
        "default": {
            "STRIP": False
        }
    }

Disable sanitation (bleach)
---------------------------
If you just want to markdownify your text, not sanitize it, add ``BLEACH: False``. Defaults to ``True``.::

    MARKDOWNIFY = {
        "default": {
            "BLEACH": False
        }
    }

Linkify text
------------
Use ``LINKIFY_TEXT`` to choose which - if any - links you want automatically to be rendered to hyperlinks. See next example for the default values:::

    MARKDOWNIFY = {
        "default": {
            "LINKIFY_TEXT": {
                "PARSE_URLS": True,

                # Next key/value-pairs only have effect if "PARSE_URLS" is True
                "PARSE_EMAIL": False,
                "CALLBACKS": [],
                "SKIP_TAGS": [],
            }
        }
    }


Use the following settings to change the linkify behavior:

Linkify email
^^^^^^^^^^^^^^
Set ``PARSE_EMAIL`` to ``True`` to automatically linkify email addresses found in your
text. Defaults to ``False``.

Set callbacks
^^^^^^^^^^^^^
Set ``CALLBACKS`` to use `callbacks <http://pythonhosted.org/bleach/linkify.html#callbacks-for-adjusting-attributes-callbacks>`_ to modify your links,
for example setting a title attribute to all your links.::

  def set_title(attrs, new=False):
      attrs[(None, u'title')] = u'link in user text'
      return attrs

  # settings.py
  ...
  "CALLBACKS": [set_title, ]
  ...

``CALLBACKS`` defaults to an empty list, so no callbacks are used. See the `bleach documentation <http://pythonhosted.org/bleach/linkify.html#callbacks-for-adjusting-attributes-callbacks>`_ for more examples.

Skip tags
^^^^^^^^^
Add tags with ``SKIP_TAGS`` to skip linkifying links within those tags, for example ``<pre>``
blocks.
For example::

  ...
  "SKIP_TAGS": ['pre', 'code', ]
  ...
