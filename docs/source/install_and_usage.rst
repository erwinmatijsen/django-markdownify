.. _install:

Installation and usage
======================


Requirements
------------
Django Markdownify requires `Django <https://www.djangoproject.com/>`_ (obviously), as well as `Markdown <https://pypi.python.org/pypi/Markdown>`_ and
`Bleach <http://pythonhosted.org/bleach/index.html>`_ version 5 or higher. When installing Django Markdownify,
dependencies will be installed automatically.


Installation
------------
Install Django Markdownify with pip:

``pip install django-markdownify``

Or add ``django-markdownify`` to your requirements.txt and run ``pip install -r requirements.txt``

Finally add ``markdownify`` to your installed apps in ``settings.py``::

  INSTALLED_APPS = [
      ...
      'markdownify.apps.MarkdownifyConfig',
  ]

Usage
-----
Load the tag in your template:

``{% load markdownify %}``

Then you can change markdown to html as follows:

``{{ 'text'|markdownify }}``


Use Markdown in your template directly::

  {% load markdownify %}
  {{'Some *test* [link](#)'|markdownify }}


Or use the filter on a variable passed to the template via your views. For example::

  # views.py
  class MarkDown(TemplateView):
      template_name = 'index.html'

      def get_context_data(self, **kwargs):
          markdowntext = open(os.path.join(os.path.dirname(__file__), 'templates/test.md')).read()

          context = super().get_context_data(**kwargs)
          context['markdowntext'] = markdowntext

          return context

  # index.html
  {% load markdownify %}
  {{ markdowntext|markdownify }}

You probably want to add some extra allowed tags and attributes in the :doc:`settings`, because the defaults are rather sparse.

It is possible to have different settings for different use cases, for example::

    # page1.html
    {{ markdowntext|markdownify }} <!-- uses the default settings -->

    # page2.html
    {{ markdowntext|markdownify:"restricted" }} <!-- uses the 'restricted' settings -->

See :doc:`settings` for a more detailed explanation.

An alternative way to use Markdownify is to put your text between the ``{% markdownify %}`` and ``{% endmmarkdownify %}`` tags::

  {% load markdownify %}

  {% markdownify %}Some *test* [link](#){% endmarkdownify %}

This is useful if you are using Markdownify on a other templatetag for example::

    {% load markdownify my_custom_template_tag %}

    {% markdownify %}
        {% mytemplatetag %}
    {% endmarkdownify %}

You can pass in the alternative settings as a parameter to the ``markdownify`` tag::

    {% load markdownify %}

    {% markdownify "restricted" %}Some *test* [link](#){% endmarkdownify %}
