import unittest

from inline_markdown import *
from generate_html import *

class TestExtractMarkdownImages(unittest.TestCase):
    def test_two_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text) ,[("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_single_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        self.assertEqual(extract_markdown_images(text), [("rick roll", "https://i.imgur.com/aKaOqIh.gif")])

    def test_no_image(self):
        text = "This has no image and has no alt text."
        self.assertEqual(extract_markdown_images(text), [])

    def test_extract_single_line_header(self):
        markdown = "# This is a header"
        expected = "This is a header"
        self.assertEqual(extract_title(markdown), expected)

