.. Markdownify documentation master file, created by
   sphinx-quickstart on Fri Jan 19 12:58:03 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.



.. toctree::
   :maxdepth: 1
   :caption: Table of contents
   :name: maintoc

   Introduction <self>
   Installation and usage <install_and_usage>
   Settings <settings>
   Tests <tests>

Django Markdownify - A Django Markdown filter
=============================================
**Django Markdownify is a template filter to convert Markdown to HTML in Django.
Markdown is converted to HTML and sanitized.**

Example::

  {% load markdownify %}
  {{'Some *test* [link](#)'|markdownify }}

Is transformed to::

  <p>
    Some <em>test</em> <a href="" rel="nofollow">link</a>
  </p>


The code can be found on `github <https://github.com/RRMoelker/django-markdownify>`_.