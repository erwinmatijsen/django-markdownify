# Django Markdown filter

Template filter to convert Markdown to HTML in Django.
Markdown is converted to HTML and sanitized.

Replacement for the deprecated: [django-markup-deprecated](https://pypi.python.org/pypi/django-markup-deprecated).

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

And add whitelisted tags to your `settings.py` file:

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

Bleach is used to sanitize potentially dangerous HTML however it can be disabled as follows:

```
MARKDOWNIFY_BLEACH = False
```

Control markdown safe mode:

```
MARKDOWNIFY_SAFEMODE = False
```

Safe mode can be one of `"remove"`, `"replace"` or `"escape"` or `False` to disable safe mode.

## Credits

This filter is a slightly richer and packaged version of the snippet: [using-markdown-django-17](http://www.jw.pe/blog/post/using-markdown-django-17/).

## Remarks

Please open a PR or create a ticket if you have something to add.
Especially if you are able to set dependency version limits.
