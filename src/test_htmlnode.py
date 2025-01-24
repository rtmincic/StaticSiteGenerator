import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        test_props = {
                        "href": "https://www.boot.dev",
                        "target": "_blank"
                     }
        node = HTMLNode(props=test_props)
        self.assertEqual(node.props_to_html(), " href=\"https://www.boot.dev\" target=\"_blank\"")

    def test_props_is_empty(self):
        test_props = {}
        node = HTMLNode(props=test_props)
        self.assertEqual(node.props_to_html(), "")

    def test_tag_exists(self):
        test_tag = "h1"
        node = HTMLNode(tag=test_tag)
        self.assertEqual(node.tag, "h1")

    def test_tag_and_value_exist(self):
        test_tag = "h1"
        test_value = "This is the value of the h1"
        node = HTMLNode(tag=test_tag, value=test_value)
        self.assertEqual(node.tag, "h1")
        self.assertEqual(node.value, "This is the value of the h1")

    def test_raise_Not_implemented(self):
        test_tag = "h1"
        node = HTMLNode(tag=test_tag)
        self.assertRaises(NotImplementedError, node.to_html)
        

