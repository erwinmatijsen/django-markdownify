# Django Markdown filter

Template filter to convert Markdown to HTML in Django.
Markdown is converted to HTML and sanitized.

It is a replacement for the deprecated [django-markup-deprecated](https://pypi.python.org/pypi/django-markup-deprecated).  It depends on [markdown](https://pypi.python.org/pypi/Markdown) and [bleach](https://pypi.python.org/pypi/bleach).

## Usage

Load the tag inside your template:

```
{% load markdownify %}
```

Then you can change markdown to html as follows:

```
{{ model|markdownify|safe }}
```

## Example

```
{% load markdownify %}
{{'Some *test* [link](#)'|markdownify|safe }}
```

Is transformed to:

```html
<p>
  Some <em>test</em> <a href="" rel="nofollow">link</a>
</p>
```


## Installation

```
pip install django-markdownify
```

or add the following to your requirements.txt

```
django-markdownify
```

Add app to installed apps in `settings.py`:

```python
'markdownify',
```

## Options
There are some optinal settings you can add to your `settings.py`.

#### Whitelist tags
Add whitelisted tags with `MARKDOWNIFY_WHITELIST_TAGS = []`  
For example:

```
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
```  
`MARKDOWNIFY_WHITELIST_TAGS` defaults to [bleach.sanitizer.ALLOWED_TAGS](https://bleach.readthedocs.io/en/latest/clean.html#allowed-tags-tags)

#### Whitelist attributes
Add whitelisted attributes with `MARKDOWNIFY_WHITELIST_ATTRS = []`  
For example:
```python
MARKDOWNIFY_WHITELIST_ATTRS = [
    'href',
    'src',
    'alt',
]
```
`MARKDOWNIFY_WHITELIST_ATTRS` defaults to [bleach.sanitizer.ALLOWED_ATTRIBUTES](https://bleach.readthedocs.io/en/latest/clean.html#allowed-attributes-attributes)

#### Strip markup
Choose if you want to strip or escape tags that aren't allowed.  
`MARKDOWNIFY_STRIP = True` (default) strips the tags.
`MARKDOWNIFY_STRIP = False` escapes them.

#### Disable sanitazion (bleach)
If you just want to markdownify your text, not sanitize it, set `MARKDOWNIFY_BLEACH = False`. Defaults to `True`.

## Credits

This filter is a slightly richer and packaged version of the snippet: [using-markdown-django-17](http://www.jw.pe/blog/post/using-markdown-django-17/).

## Remarks

Please open a PR or create a ticket if you have something to add.
Especially if you are able to set dependency version limits.
