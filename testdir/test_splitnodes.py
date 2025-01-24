from src.textnode import TextNode, TextType
from src.important_functions import split_nodes_delimiter
import unittest
import re

class SplitNodesDelimiterTest(unittest.TestCase):

    def test_no_delimiter(self):
        old_nodes = [TextNode("This is a test", TextType.NORMAL)]
        delimiter = "|"
        text_type = TextType.BOLD  # Example text type
        expected_nodes = [TextNode("This is a test", TextType.NORMAL)]
        self.assertEqual(split_nodes_delimiter(old_nodes, delimiter, text_type), expected_nodes)

    def test_even_delimiters(self):
        old_nodes = [TextNode("This |is| a |test|", TextType.NORMAL)]
        delimiter = "|"
        text_type = TextType.BOLD
        expected_nodes = [
            TextNode("This ", TextType.NORMAL),
            TextNode("is", TextType.BOLD),
            TextNode(" a ", TextType.NORMAL),
            TextNode("test", TextType.BOLD),
            TextNode("", TextType.NORMAL),  # Trailing empty node
        ]
        self.assertEqual(split_nodes_delimiter(old_nodes, delimiter, text_type), expected_nodes)

    def test_odd_delimiters(self):
        old_nodes = [TextNode("This |is| a |test", TextType.NORMAL)]
        delimiter = "|"
        text_type = TextType.BOLD
        with self.assertRaisesRegex(Exception, "There is a missing closing delimiter"):
            split_nodes_delimiter(old_nodes, delimiter, text_type)

    def test_mixed_node_types(self):
        old_nodes = [
            TextNode("This is normal", TextType.NORMAL),
            TextNode("This is |bold|", TextType.NORMAL),
            TextNode("This is already bold", TextType.BOLD),
        ]
        delimiter = "|"
        text_type = TextType.BOLD
        expected_nodes = [
            TextNode("This is normal", TextType.NORMAL),
            TextNode("This is ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode("", TextType.NORMAL),  # Trailing empty node
            TextNode("This is already bold", TextType.BOLD),
        ]
        self.assertEqual(split_nodes_delimiter(old_nodes, delimiter, text_type), expected_nodes)

    def test_empty_node(self):
        old_nodes = [TextNode("", TextType.NORMAL)]
        delimiter = "|"
        text_type = TextType.BOLD
        expected_nodes = [TextNode("", TextType.NORMAL)]
        self.assertEqual(split_nodes_delimiter(old_nodes, delimiter, text_type), expected_nodes)

    def test_delimiter_at_start_and_end(self):
        old_nodes = [TextNode("|This is a test|", TextType.NORMAL)]
        delimiter = "|"
        text_type = TextType.BOLD
        expected_nodes = [
            TextNode("", TextType.NORMAL),
            TextNode("This is a test", TextType.BOLD),
            TextNode("", TextType.NORMAL),  # Trailing empty node
        ]
        self.assertEqual(split_nodes_delimiter(old_nodes, delimiter, text_type), expected_nodes)



