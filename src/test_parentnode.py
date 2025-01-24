import unittest

from htmlnode import *

class TestParentNode(unittest.TestCase):
    def test_everything(self):
        node = ParentNode("p", 
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
        {
                            "href": "https://www.boot.dev",
                            "target": "_blank"
        }
        )
        self.assertEqual(node.to_html(), "<p href=\"https://www.boot.dev\" target=\"_blank\"><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_no_props(self):
        node = ParentNode("p", 
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],)
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_no_children(self):
        with self.assertRaises(ValueError):
            node = ParentNode("p", None)
            node.to_html()

    def test_no_tag(self):
        with self.assertRaises(ValueError):
            node = ParentNode(None,[
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
            ],)
            node.to_html()

    def test_node_within_node(self):
        node = ParentNode("p",
                        [LeafNode("b", "Bold Text"),
                        ParentNode("p", [
                                        LeafNode("i", "Italic text"),
                                         LeafNode("h1", "Header text")
                                        ]),
                        LeafNode("a", "Link Text")  
                        ]
                        )
        self.assertEqual(node.to_html(), "<p><b>Bold Text</b><p><i>Italic text</i><h1>Header text</h1></p><a>Link Text</a></p>")
