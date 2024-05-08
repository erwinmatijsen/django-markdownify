# Django Markdownify - A Django Markdown filter

![PyPi Downloads](https://img.shields.io/pypi/dm/django-markdownify) 
![License](https://img.shields.io/pypi/l/django-markdownify?color=brightgreen)
[![Documentation Status](https://readthedocs.org/projects/django-markdownify/badge/?version=latest)](https://django-markdownify.readthedocs.io/en/latest/?badge=latest)
![Version](https://img.shields.io/pypi/v/django-markdownify)

Django Markdownify is a template filter to convert Markdown to HTML in Django. Markdown is converted to HTML and sanitized.

Read the full documentation on [Read the docs](http://django-markdownify.readthedocs.io/en/latest/) or check out the package on [pypi](https://pypi.python.org/pypi/django-markdownify).

> [!WARNING]  
> The [old settings](https://django-markdownify.readthedocs.io/en/latest/settings-old.html#oldsettings) are removed in release 0.9.4! Please update to the [new settings](https://django-markdownify.readthedocs.io/en/latest/settings.html) as soon as possible.

## Usage

Load the tag inside your template:

```
{% load markdownify %}
```

Then you can change markdown to html as follows:

```
{{ 'text'|markdownify }}
```

or

```
{{ somevariable|markdownify }}
```

## Example

```
{% load markdownify %}
{{'Some *test* [link](#)'|markdownify }}
```

Is transformed to:

```html
<p>
  Some <em>test</em> <a href="#">link</a>
</p>
```

The filter is a wrapper around [Markdown](https://pypi.python.org/pypi/Markdown) and
[Bleach](http://pythonhosted.org/bleach/index.html) and as such supports their settings. 
It is possible to define multiple settings for multiple usecases.

For example:

```python
# settings.py

MARKDOWNIFY = {
  "default": {
     "WHITELIST_TAGS": ["a", "p", "h1", ]
  },

  "alternative": {
     "WHITELIST_TAGS": ["a", "p", ],
     "MARKDOWN_EXTENSIONS": ["markdown.extensions.fenced_code", ]
  }
}
```

And in your templates:

```html

<!-- page1.html -->
{{ mytext|markdownify }} <!-- Uses your default settings -->

<!-- page2.html -->
{{ mytext|markdownify:"alternative" }} <!-- Uses your alternative settings -->
```

## Documentation
Read the full documentation on [Read the docs](https://django-markdownify.readthedocs.io/en/latest/).

## Credits
This filter is a slightly richer and packaged version of the snippet: [using-markdown-django-17](http://www.jw.pe/blog/post/using-markdown-django-17/).
