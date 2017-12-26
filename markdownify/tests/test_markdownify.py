from django.test import SimpleTestCase, override_settings
from django.conf import settings
from markdownify.templatetags.markdownify import markdownify

import os


class MarkdownifyTestCase(SimpleTestCase):

    maxDiff = None

    def setUp(self):

        self.input_text = open(os.path.join(os.path.dirname(__file__), 'input_text.md')).read()

    @override_settings()
    def test_default_tags(self):
        """
        If no options are given in settings.py, use default settings from bleach.
        NB: acronym is deprecated in HTML5
        NB: rel="nofollow" is added after sanitizing with bleach.linkify
        """

        # Delete all bleach related settings
        del settings.MARKDOWNIFY_WHITELIST_TAGS,
        del settings.MARKDOWNIFY_WHITELIST_ATTRS,
        del settings.MARKDOWNIFY_WHITELIST_STYLES,
        del settings.MARKDOWNIFY_WHITELIST_PROTOCOLS,
        del settings.MARKDOWNIFY_STRIP,
        del settings.MARKDOWNIFY_BLEACH,

        # Set MARKDOWNIFY_MARKDOWN_EXTENSIONS to test abbr
        settings.MARKDOWNIFY_MARKDOWN_EXTENSIONS = ['markdown.extensions.extra', ]

        output = markdownify(self.input_text)

        expected_output = """
        <a href="http://somelink.com" rel="nofollow" title="somelink">This</a> is <strong>not</strong> an 
        <abbr title="abbrevation">abbr</abbr>. It <em>is</em> however a <acronym title="acronym">accr</acronym>.
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
