from django.test import SimpleTestCase, override_settings
from django.conf import settings
from markdownify.templatetags.markdownify import markdownify

import os


class MarkdownifyTestCase(SimpleTestCase):

    maxDiff = None

    def setUp(self):

        self.input_text_default = open(os.path.join(os.path.dirname(__file__), 'input_text_default.md')).read()
        self.input_text_extensions = open(os.path.join(os.path.dirname(__file__), 'input_text_extensions.md')).read()

    @override_settings()
    def test_default_settings(self):
        """
        If no options are given in settings.py, use default settings from bleach.
        NB: acronym is deprecated in HTML5
        NB: rel="nofollow" is added after sanitizing with bleach.linkify
        """

        # Delete all bleach related settings
        del settings.MARKDOWNIFY_WHITELIST_TAGS
        del settings.MARKDOWNIFY_WHITELIST_ATTRS
        del settings.MARKDOWNIFY_WHITELIST_STYLES
        del settings.MARKDOWNIFY_WHITELIST_PROTOCOLS
        del settings.MARKDOWNIFY_STRIP
        del settings.MARKDOWNIFY_BLEACH

        # Set MARKDOWNIFY_MARKDOWN_EXTENSIONS to test abbr
        settings.MARKDOWNIFY_MARKDOWN_EXTENSIONS = ['markdown.extensions.extra', ]

        output = markdownify(self.input_text_default)
        expected_output = """
        <a href="http://somelink.com" rel="nofollow" title="somelink">This</a> is <strong>not</strong> an 
        <abbr title="abbrevation">abbr</abbr>. It <em>is</em> however an <acronym title="acronym">accr</acronym>.
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
        <a href="http://httplink.com" rel="nofollow">http-link</a>, 
        <a href="https://httpslink.com" rel="nofollow">https-link</a>,
        <a href="mailto:somebody@example.com">mailto-link</a>,
        <a>ftp-link</a>.
        
        And last but not least, there are some <i>tags</i> to <b>test</b>.
        <blockquote>Like this blockquote.</blockquote>
        
        This <a href="#" rel="nofollow">link</a> has a target.
        """

        self.assertHTMLEqual(output, expected_output)

    @override_settings()
    def test_custom_settings(self):
        """
        If options are set in settings.py, default values of bleach.sanitize should be overriden.
        NB: rel="nofollow" is added after sanitizing with bleach.linkify
        """

        # Set some settings
        settings.MARKDOWNIFY_WHITELIST_TAGS = ['p', 'a', ]
        settings.MARKDOWNIFY_WHITELIST_ATTRS = ['href', 'style', ]
        settings.MARKDOWNIFY_WHITELIST_STYLES = ['color', 'font-weight', 'border', ]
        settings.MARKDOWNIFY_WHITELIST_PROTOCOLS = ['http', 'ftp', ]
        settings.MARKDOWNIFY_STRIP = True
        settings.MARKDOWNIFY_BLEACH = True

        # Set MARKDOWNIFY_MARKDOWN_EXTENSIONS to test abbr
        settings.MARKDOWNIFY_MARKDOWN_EXTENSIONS = ['markdown.extensions.extra', ]

        output = markdownify(self.input_text_default)
        expected_output = """
        <p><a href="http://somelink.com" rel="nofollow">This</a> is not an abbr. It is however an accr.
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
        <a href="http://httplink.com" rel="nofollow">http-link</a>, 
        <a>https-link</a>,
        <a>mailto-link</a>,
        <a href="ftp://ftpserver.com" rel="nofollow">ftp-link</a>.</p>

        <p>And last but not least, there are some tags to test.</p>
        <p>Like this blockquote.</p>
        <p>This <a href="#" rel="nofollow">link</a> has a target.</p>
        """

        self.assertHTMLEqual(output, expected_output)

    @override_settings()
    def test_extensions(self):
        """
        Test if Python Markdown extensions are working.
        """

        # Set default settings, and tags
        settings.MARKDOWNIFY_WHITELIST_TAGS = ['p', 'pre', ]
        del settings.MARKDOWNIFY_WHITELIST_ATTRS
        del settings.MARKDOWNIFY_WHITELIST_STYLES
        del settings.MARKDOWNIFY_WHITELIST_PROTOCOLS
        del settings.MARKDOWNIFY_STRIP
        del settings.MARKDOWNIFY_BLEACH

        # Enable a included extension
        settings.MARKDOWNIFY_MARKDOWN_EXTENSIONS = ['markdown.extensions.fenced_code', ]
        output = markdownify(self.input_text_extensions)

        expected_output = """
            <p>Fenced code:</p>
            <pre>def test(y): print(y)</pre>
            """

        self.assertHTMLEqual(output, expected_output)

        # Disable extensions
        del settings.MARKDOWNIFY_MARKDOWN_EXTENSIONS

        output = markdownify(self.input_text_extensions)

        expected_output = """
                    <p>Fenced code:
                    ~~~~~~~~~~~~~~~~~~~~{.python}
                    def test(y):  
                        print(y)  
                    ~~~~~~~~~~~~~~~~~~~~</p>
                    """

        self.assertHTMLEqual(output, expected_output)