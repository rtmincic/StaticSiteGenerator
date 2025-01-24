import unittest

from htmlnode import LeafNode
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_diff(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a different node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_diff_none_url(self):
        node = TextNode("This is a Text node", TextType.CODE, "http://www.boot.dev")
        node2 = TextNode("This is a Text node", TextType.CODE)
        self.assertNotEqual(node, node2)

    def test_diff_text_type(self):
        node = TextNode("This is a Text node", TextType.BOLD)
        node2 = TextNode("This is a Text node", TextType.CODE)
        self.assertNotEqual(node, node2)

    def test_diff_url(self):
        node = TextNode("This is a Text node", TextType.BOLD, "somewebsite")
        node2 = TextNode("This is a Text node", TextType.BOLD, "awebsite")
        self.assertNotEqual(node, node2)

    def test_diff_text(self):
        node = TextNode("This is a Text node", TextType.BOLD, "awebsite")
        node2 = TextNode("This is a Text nodes", TextType.BOLD, "awebsite")
        self.assertNotEqual(node, node2)

    def test_bold_to_html(self):
        node = TextNode("This is a BOLD node", TextType.BOLD)
        self.assertEqual(node.self_to_html_node().to_html(), LeafNode("b", "This is a BOLD node").to_html())

