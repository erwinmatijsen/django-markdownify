.. _oldsettings:

Settings (Prior to 0.9.0)
=====================

.. warning:: The settings described here are for version 0.9 and down. The old style settings are removed since version 0.9.4. For reference, you can find the deprecated settings here: :ref:`oldsettings`

You can change the behavior of Markdownify by adding them to your ``settings.py``. All settings are optional and will
fall back to default behavior if not specified.


Whitelist tags
--------------
Add whitelisted tags with ``MARKDOWNIFY_WHITELIST_TAGS = []``
For example::

  MARKDOWNIFY_WHITELIST_TAGS = [
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

``MARKDOWNIFY_WHITELIST_TAGS`` defaults to `bleach.sanitizer.ALLOWED_TAGS <https://bleach.readthedocs.io/en/latest/clean.html#allowed-tags-tags>`_

Whitelist attributes
--------------------
Add whitelisted attributes with ``MARKDOWNIFY_WHITELIST_ATTRS = []``
For example::

    MARKDOWNIFY_WHITELIST_ATTRS = [
        'href',
        'src',
        'alt',
    ]


``MARKDOWNIFY_WHITELIST_ATTRS`` defaults to `bleach.sanitizer.ALLOWED_ATTRIBUTES <https://bleach.readthedocs.io/en/latest/clean.html#allowed-attributes-attributes>`_

Whitelist styles
----------------
Add whitelisted styles with ``MARKDOWNIFY_WHITELIST_STYLES = []``
For example::

    MARKDOWNIFY_WHITELIST_STYLES = [
        'color',
        'font-weight',
    ]

``MARKDOWNIFY_WHITELIST_STYLES`` defaults to `bleach.sanitizer.ALLOWED_STYLES <https://bleach.readthedocs.io/en/latest/clean.html#allowed-styles-styles>`_ (Note that it's an empty list)

Whitelist protocols
-------------------
Add whitelisted protocols with ``MARKDOWNIFY_WHITELIST_PROTOCOLS = []``
For example::

    MARKDOWNIFY_WHITELIST_PROTOCOLS = [
        'http',
        'https',
    ]

``MARKDOWNIFY_WHITELIST_PROTOCOLS`` defaults to `bleach.sanitizer.ALLOWED_PROTOCOLS <https://bleach.readthedocs.io/en/latest/clean.html#allowed-protocols-protocols>`_


Enable Markdown Extensions
--------------------------
`Python-Markdown <https://python-markdown.github.io/>`_ is extensible with extensions. To enable one or more extensions,
add ``MARKDOWNIFY_MARKDOWN_EXTENSIONS`` to your ``settings.py``.
For example::

  MARKDOWNIFY_MARKDOWN_EXTENSIONS = ['markdown.extensions.fenced_code',
                                     'markdown.extensions.extra', ]

``MARKDOWNIFY_MARKDOWN_EXTENSIONS`` defaults to an empty list (so no extensions are used).
To read more about extensions and see the list of official supported extensions,
go to `the markdown documentation <https://python-markdown.github.io/extensions/>`_.


Strip markup
------------
Choose if you want to `strip or escape <http://pythonhosted.org/bleach/clean.html#stripping-markup-strip>`_ tags that aren't allowed.
``MARKDOWNIFY_STRIP = True`` (default) strips the tags.
``MARKDOWNIFY_STRIP = False`` escapes them.


Disable sanitation (bleach)
---------------------------
If you just want to markdownify your text, not sanitize it, set ``MARKDOWNIFY_BLEACH = False``. Defaults to ``True``.

Linkify text
------------
Use ``MARKDOWNIFY_LINKIFY_TEXT`` to choose if you automatically want your links to be rendered to hyperlinks. Defaults to ``MARKDOWNIFY_LINKIFY_TEXT = True``. If ``True``, links will be linkified but emailaddresses won't.

Use the following settings to change the linkify behavior:

Linkify email
^^^^^^^^^^^^^^
Set ``MARKDOWNIFY_LINKIFY_PARSE_EMAIL`` to ``True`` or ``False`` to automatically linkify emailaddresses found in your
text. Defaults to ``False``.

Set callbacks
^^^^^^^^^^^^^
Set ``MARKDOWNIFY_LINKIFY_CALLBACKS`` to use `callbacks <http://pythonhosted.org/bleach/linkify.html#callbacks-for-adjusting-attributes-callbacks>`_ to modify your links,
for example setting a title attribute to all your links.::

  def set_title(attrs, new=False):
      attrs[(None, u'title')] = u'link in user text'
      return attrs

  # settings.py
  MARKDOWNIFY_LINKIFY_CALLBACKS = [set_title, ]

``MARKDOWNIFY_LINKIFY_CALLBACKS`` defaults to ``None``, so no callbacks are used. See the `bleach documentation <http://pythonhosted.org/bleach/linkify.html#callbacks-for-adjusting-attributes-callbacks>`_ for more examples.

Skip tags
^^^^^^^^^
Add tags with ``MARKDOWNIFY_LINKIFY_SKIP_TAGS = []`` to skip linkifying links within those tags, for example ``<pre>``
blocks.
For example::

  MARKDOWNIFY_LINKIFY_SKIP_TAGS = ['pre', 'code', ]

