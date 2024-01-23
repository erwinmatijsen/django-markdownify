from django.test import SimpleTestCase, override_settings
from django.conf import settings
from django.template import Context, Template, TemplateSyntaxError

from markdownify.templatetags.markdownify import markdownify

import os


class MarkdownifyTestCase(SimpleTestCase):
    maxDiff = None

    @override_settings()
    def setUp(self):

        # Read in texts
        self.input_text_default = open(os.path.join(os.path.dirname(__file__), 'input_text_default.md')).read()
        self.input_text_extensions = open(os.path.join(os.path.dirname(__file__), 'input_text_extensions.md')).read()
        self.input_text_bleach = open(os.path.join(os.path.dirname(__file__), 'input_text_bleach.md')).read()
        self.input_text_strip = open(os.path.join(os.path.dirname(__file__), 'input_text_strip.md')).read()
        self.input_text_linkify = open(os.path.join(os.path.dirname(__file__), 'input_text_linkify.md')).read()
        self.input_text_alternative = open(os.path.join(os.path.dirname(__file__), 'input_text_alternative.md')).read()

    @override_settings()
    def test_default_settings(self):
        """
        If no bleach related options are given in settings.py, use default settings.
        """

        # Delete settings
        del settings.MARKDOWNIFY

        output = markdownify(self.input_text_default)
        expected_output = """
        <a href="http://somelink.com" title="somelink">This</a> is <strong>not</strong> a real link. 
        It <em>is</em> however an <acronym title="acronym">accr</acronym>.
        Here, have piece of <code>code</code>. And two lists. 

        This is list one: 
        <ul>
            <li>Item 1</li>
            <li>Item 2</li>
        </ul>

        This is list two: 
        <ol>
            <li>Item 1</li>
            <li>Item 2</li>
        </ol>

        This paragraph has some inline styling.

        In this paragraph, protocols are being tested. 
        <a href="http://httplink.com">http-link</a>, 
        <a href="https://httpslink.com">https-link</a>,
        <a href="mailto:somebody@example.com">mailto-link</a>,
        <a>ftp-link</a>.

        And last but not least, there are some <i>tags</i> to <b>test</b>.
        <blockquote>Like this blockquote.</blockquote>

        This <a href="#">link</a> has a target.
        """

        self.assertHTMLEqual(output, expected_output)

    @override_settings()
    def test_custom_settings(self):
        """
        If options are set in settings.py, default values of bleach.sanitize should be overridden.
        """

        # Delete settings
        del settings.MARKDOWNIFY

        # Set some settings
        settings.MARKDOWNIFY = {
            "default": {
                "WHITELIST_TAGS": ['p', 'a', ],
                "WHITELIST_ATTRS": ['href', 'style', ],
                "WHITELIST_STYLES": ['color', 'font-weight', 'border', ],
                "WHITELIST_PROTOCOLS": ['http', 'ftp', ],
                "MARKDOWN_EXTENSIONS": ['markdown.extensions.extra', ],
                "STRIP": True,
                "BLEACH": True
            }
        }

        output = markdownify(self.input_text_default)
        expected_output = """
        <p><a href="http://somelink.com">This</a> is not a real link. It is however an accr.
        Here, have piece of code. And two lists.</p>

        <p>This is list one:</p> 
        Item 1
        Item 2

        <p>This is list two:</p> 
        Item 1
        Item 2

        <p style="color: red; font-weight: 900; border: 1px solid blue;">
        This paragraph has some inline styling.</p>

        <p>In this paragraph, protocols are being tested. 
        <a href="http://httplink.com">http-link</a>, 
        <a>https-link</a>,
        <a>mailto-link</a>,
        <a href="ftp://ftpserver.com">ftp-link</a>.</p>

        <p>And last but not least, there are some tags to test.</p>
        <p>Like this blockquote.</p>
        <p>This <a href="#">link</a> has a target.</p>
        """

        self.assertHTMLEqual(output, expected_output)

    @override_settings()
    def test_extensions(self):
        """
        Test if Python Markdown extensions are working.
        """

        # Delete settings
        del settings.MARKDOWNIFY

        # Set default settings, and tags
        settings.MARKDOWNIFY = {
            "default": {
                "WHITELIST_TAGS": ['p', 'pre', ],  # Some defaults
                "MARKDOWN_EXTENSIONS": ['markdown.extensions.fenced_code', ]  # Enable an included extension
            }
        }

        output = markdownify(self.input_text_extensions)

        expected_output = """
            <p>Fenced code:</p>
            <pre>def test(y): print(y)</pre>
            """

        self.assertHTMLEqual(output, expected_output)

        # Disable extensions
        del settings.MARKDOWNIFY["default"]["MARKDOWN_EXTENSIONS"]

        output = markdownify(self.input_text_extensions)
        expected_output = """
                    <p>Fenced code:
                    ~~~~~~~~~~~~~~~~~~~~{.python}
                    def test(y):  
                        print(y)  
                    ~~~~~~~~~~~~~~~~~~~~</p>
                    """

        self.assertHTMLEqual(output, expected_output)

    @override_settings()
    def test_extension_configs(self):
        """
        Test if configs for extensions are working
        """

        # Delete settings
        del settings.MARKDOWNIFY

        # Set default settings, and tags
        settings.MARKDOWNIFY = {
            "default": {
                "WHITELIST_TAGS": ['p', 'pre', 'code'],
                "WHITELIST_ATTRS": ['class', ],
                "MARKDOWN_EXTENSIONS": ['fenced_code', ],  # Enable an included extension
                "MARKDOWN_EXTENSION_CONFIGS": {
                    "fenced_code": {
                        "lang_prefix": "test-"  # Change default setting from 'language-' to 'test-'
                    }
                }
            }
        }

        output = markdownify(self.input_text_extensions)
        expected_output = """
            <p>Fenced code:</p>
            <pre><code class="test-python">def test(y): print(y)</code></pre>
            """
        self.assertHTMLEqual(output, expected_output)

        # Revert setting
        del settings.MARKDOWNIFY["default"]["MARKDOWN_EXTENSION_CONFIGS"]
        output = markdownify(self.input_text_extensions)
        expected_output = """
            <p>Fenced code:</p>
            <pre><code class="language-python">def test(y): print(y)</code></pre>
            """
        self.assertHTMLEqual(output, expected_output)

    @override_settings()
    def test_no_bleach(self):
        """
        Test enabling and disabling of bleach
        """

        # Delete settings
        del settings.MARKDOWNIFY

        # With bleach (and default settings)
        settings.MARKDOWNIFY = {
            "default": {
                "BLEACH": True
            }
        }

        output = markdownify(self.input_text_bleach)
        expected_output = """
            Bleach
            Bleach is an allowed-list-based HTML sanitizing library that escapes or strips markup and attributes.
            <a href="https://bleach.readthedocs.io/en/latest/index.html">Website</a>
            """

        self.assertHTMLEqual(output, expected_output)

        # Without bleach
        settings.MARKDOWNIFY["default"]["BLEACH"] = False
        output = markdownify(self.input_text_bleach)

        expected_output = """
            <h1>Bleach</h1>
            <p>Bleach is an allowed-list-based HTML sanitizing library that escapes or strips 
            markup and attributes.</p>
            <p><a href="https://bleach.readthedocs.io/en/latest/index.html">Website</a></p>
            """
        self.assertHTMLEqual(output, expected_output)

    @override_settings()
    def test_strip(self):
        """
        Test disabling of stripping
        """

        # Delete settings
        del settings.MARKDOWNIFY

        # With stripping enabled (default)
        settings.MARKDOWNIFY = {
            "default": {
                "BLEACH": True,
                "WHITELIST_TAGS": ["h1", "p", ],
                "STRIP": True
            }
        }

        output = markdownify(self.input_text_strip)
        expected_output = """
        <h1>Strip</h1>
        <p>This is a short paragraph with some tags that can be stripped.</p>
        """
        self.assertHTMLEqual(output, expected_output)

        # Without stripping
        settings.MARKDOWNIFY["default"]["STRIP"] = False

        output = markdownify(self.input_text_strip)
        expected_output = """
        <h1>Strip</h1>
        <p>This is a short paragraph with some &lt;em&gt;tags&lt;/em&gt; that can be stripped.</p>
        """
        self.assertHTMLEqual(output, expected_output)

    @override_settings()
    def test_linkify(self):
        """
        Test bleach linkify defaults
        """

        # Delete settings
        del settings.MARKDOWNIFY

        # Set some settings
        settings.MARKDOWNIFY = {
            "default": {
                "WHITELIST_TAGS": ['h1', 'p', 'a', ],
                "WHITELIST_ATTRS": ['href', ],
            }
        }

        output = markdownify(self.input_text_linkify)
        expected_output = """
            <h1>Linkify</h1>
            <p>
              <a href="http://somelink.com">http://somelink.com</a>
              someone@somecompany.com
              <a href="http://somelink.com">Website</a>
            </p>
        """

        self.assertHTMLEqual(output, expected_output)

    @override_settings()
    def test_linkify_no_linkify(self):
        """
        Test bleach linkify turned off
        """

        # Delete settings
        del settings.MARKDOWNIFY

        # Set some settings, turn off linkify completely
        settings.MARKDOWNIFY = {
            "default": {
                "WHITELIST_TAGS": ['h1', 'p', 'a', ],
                "WHITELIST_ATTRS": ['href', ],
                "LINKIFY_TEXT": {
                    "PARSE_URLS": False
                }
            }
        }

        output = markdownify(self.input_text_linkify)

        expected_output = """
            <h1>Linkify</h1>
            <p>http://somelink.com
               someone@somecompany.com
               <a href="http://somelink.com">Website</a>
            </p>
        """

        self.assertHTMLEqual(output, expected_output)

    @override_settings()
    def test_linkify_linkify_email(self):
        """
        Test bleach linkify email
        """

        # Delete settings
        del settings.MARKDOWNIFY

        # Set some settings
        settings.MARKDOWNIFY = {
            "default": {
                "WHITELIST_TAGS": ['h1', 'p', 'a', ],
                "WHITELIST_ATTRS": ['href', ],
                "LINKIFY_TEXT": {
                    "PARSE_URLS": True,
                    "PARSE_EMAIL": True
                }
            }
        }
        output = markdownify(self.input_text_linkify)

        expected_output = """
            <h1>Linkify</h1>
            <p>
              <a href="http://somelink.com">http://somelink.com</a>
              <a href="mailto:someone@somecompany.com">someone@somecompany.com</a>
              <a href="http://somelink.com">Website</a>
            </p>
        """

        self.assertHTMLEqual(output, expected_output)

    @override_settings()
    def test_alternative_settings(self):
        """
        Test alternative settings
        """

        # Delete settings
        del settings.MARKDOWNIFY

        # Set alternative settings
        settings.MARKDOWNIFY = {
            "default": {
                "WHITELIST_TAGS": ['h1', 'p', ]
            },
            "alternative": {
                "WHITELIST_TAGS": ['p', ]
            }
        }

        output_default = markdownify(self.input_text_alternative)
        output_alternative = markdownify(self.input_text_alternative, custom_settings="alternative")

        self.assertNotEqual(output_default, output_alternative)

        expected_default = """
        <h1>Header 1</h1>
        <p>Some paragraph text</p>
        """

        expected_alternative = """
        Header 1
        <p>Some paragraph text</p>
        """

        self.assertHTMLEqual(expected_default, output_default)
        self.assertHTMLEqual(expected_alternative, output_alternative)

    @override_settings()
    def test_markdownify_nodelist(self):
        """
        Test markdownify with a nodelist, e.g. {% markdownify %}{{ text }}{% endmarkdownify %}
        """

        # Delete settings
        del settings.MARKDOWNIFY

        # Set some settings
        settings.MARKDOWNIFY = {
            "default": {
                "WHITELIST_TAGS": ['h1', ],
            }
        }

        text = "# Some header \n## Some subheader\nLorem ipsum"
        out = Template(
            "{% load markdownify %}"
            "{% markdownify %}"
            "{{ text }}"
            "{% endmarkdownify %}"
        ).render(Context({"text": text}))

        expected_output = """
        <h1>Some header</h1> 
        
        Some subheader
        
        Lorem ipsum
        """

        self.assertHTMLEqual(expected_output, out)
