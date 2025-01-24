import unittest

from src.htmlnode import HTMLNode, LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html(self):
        test_prop = {
                        "href": "https://www.boot.dev",
                        "target": "_blank"
                     }
        node = LeafNode("p", "This is a paragraph tags value", test_prop)
        self.assertEqual(node.to_html(), "<p href=\"https://www.boot.dev\" target=\"_blank\">This is a paragraph tags value</p>")

    def test_leaf_with_no_props(self):
        node = LeafNode("h1", "This is header 1's value")
        self.assertEqual(node.to_html(), "<h1>This is header 1's value</h1>")

    def test_no_tag(self):
        node = LeafNode(tag=None, value="This is a tagless value")
        self.assertEqual(node.to_html(), "This is a tagless value")

    def test_no_value(self):
        with self.assertRaises(ValueError):
            node = LeafNode("p" , None)
            node.to_html()
