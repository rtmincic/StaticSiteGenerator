import unittest
from markdown_blocks import *

class SplitNodesDelimiterTest(unittest.TestCase):
    def test_paragraph(self):
        node = markdown_to_html_node("This is a paragraph")
        assert node.tag == "div"
        assert len(node.children) == 1
        assert node.children[0].tag == "p"
        assert node.children[0].children[0].tag == "text"
        assert node.children[0].children[0].value == "This is a paragraph"

    def test_code_block(self):
            node = markdown_to_html_node("```\nprint('hello')\n```")
            assert node.tag == "div"
            assert len(node.children) == 1
            assert node.children[0].tag == "pre"
            assert node.children[0].children[0].tag == "code"
            assert node.children[0].children[0].children[0].value == "print('hello')"

    def test_unordered_list(self):
        markdown = """- First item
    - Second item
    - Third item"""
        node = markdown_to_html_node(markdown)
        assert node.children[0].tag == "ul"
        assert len(node.children[0].children) == 3
        assert node.children[0].children[0].tag == "li"
        assert node.children[0].children[0].children[0].value == "First item"
    
    def test_mixed_list_styles(self):
        markdown = """- First item
    * Second item
    - Third item"""
        node = markdown_to_html_node(markdown)
        assert node.children[0].tag == "ul"
        assert len(node.children[0].children) == 3

    def test_paragraph_with_formatting(self):
        markdown = "This is *italic* and **bold** text with `code`"
        node = markdown_to_html_node(markdown)
        assert node.children[0].tag == "p"
        assert len(node.children[0].children) > 1  # Should have multiple child nodes

    def test_nested_formatting(self):
        markdown = "**Bold text with *italic* inside**"
        node = markdown_to_html_node(markdown)
        assert node.children[0].tag == "p"

    def test_multiple_paragraphs(self):
        markdown = """First paragraph
        
    Second paragraph"""
        node = markdown_to_html_node(markdown)
        assert len(node.children) == 2
        assert node.children[0].tag == "p"
        assert node.children[1].tag == "p"

