from textnode import TextNode, TextType
from important_functions import split_nodes_delimiter, split_nodes_link, split_nodes_image, markdown_to_blocks
import unittest
import re

class SplitNodesDelimiterTest(unittest.TestCase):

    def test_no_delimiter(self):
        old_nodes = [TextNode("This is a test", TextType.TEXT)]
        delimiter = "|"
        text_type = TextType.BOLD  # Example text type
        expected_nodes = [TextNode("This is a test", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter(old_nodes, delimiter, text_type), expected_nodes)

    def test_even_delimiters(self):
        old_nodes = [TextNode("This |is| a |test|", TextType.TEXT)]
        delimiter = "|"
        text_type = TextType.BOLD
        expected_nodes = [
            TextNode("This ", TextType.TEXT),
            TextNode("is", TextType.BOLD),
            TextNode(" a ", TextType.TEXT),
            TextNode("test", TextType.BOLD),
            TextNode("", TextType.TEXT),  # Trailing empty node
        ]
        self.assertEqual(split_nodes_delimiter(old_nodes, delimiter, text_type), expected_nodes)

    def test_odd_delimiters(self):
        old_nodes = [TextNode("This |is| a |test", TextType.TEXT)]
        delimiter = "|"
        text_type = TextType.BOLD
        with self.assertRaisesRegex(Exception, "There is a missing closing delimiter"):
            split_nodes_delimiter(old_nodes, delimiter, text_type)

    def test_mixed_node_types(self):
        old_nodes = [
            TextNode("This is normal", TextType.TEXT),
            TextNode("This is |bold|", TextType.TEXT),
            TextNode("This is already bold", TextType.BOLD),
        ]
        delimiter = "|"
        text_type = TextType.BOLD
        expected_nodes = [
            TextNode("This is normal", TextType.TEXT),
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("", TextType.TEXT),  # Trailing empty node
            TextNode("This is already bold", TextType.BOLD),
        ]
        self.assertEqual(split_nodes_delimiter(old_nodes, delimiter, text_type), [
            TextNode("This is normal", TextType.TEXT),
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("", TextType.TEXT),  # Trailing empty node
            TextNode("This is already bold", TextType.BOLD),
        ])

    def test_empty_node(self):
        old_nodes = [TextNode("", TextType.TEXT)]
        delimiter = "|"
        text_type = TextType.BOLD
        expected_nodes = [TextNode("", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter(old_nodes, delimiter, text_type), expected_nodes)

    def test_delimiter_at_start_and_end(self):
        old_nodes = [TextNode("|This is a test|", TextType.TEXT)]
        delimiter = "|"
        text_type = TextType.BOLD
        expected_nodes = [
            TextNode("", TextType.TEXT),
            TextNode("This is a test", TextType.BOLD),
            TextNode("", TextType.TEXT),  # Trailing empty node
        ]
        self.assertEqual(split_nodes_delimiter(old_nodes, delimiter, text_type), expected_nodes)

    def test_multiple_links(self):
        old_nodes = [TextNode("This has two links. First link: [to boot dev](www.boot.dev) and here is the second link: [to google](www.google.com)", TextType.TEXT)]
        expected_nodes = [
            TextNode("This has two links. First link: ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "www.boot.dev"),
            TextNode(" and here is the second link: ", TextType.TEXT),
            TextNode("to google", TextType.LINK, "www.google.com")
        ]
        self.assertEqual(split_nodes_link(old_nodes), expected_nodes)

    def test_multiple_links_with_multiple_nodes(self):
        old_nodes = [TextNode("This has two links. First link: [to boot dev](www.boot.dev) and here is the second link: [to google](www.google.com)", TextType.TEXT),
                     TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)
                     ]
        expected_nodes = [
            TextNode("This has two links. First link: ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "www.boot.dev"),
            TextNode(" and here is the second link: ", TextType.TEXT),
            TextNode("to google", TextType.LINK, "www.google.com"),
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            )
        ]
        self.assertEqual(split_nodes_link(old_nodes), expected_nodes)

    def test_multiple_links_with_multiple_nodes_text_at_end(self):
        old_nodes = [TextNode("This has two links. First link: [to boot dev](www.boot.dev) and here is the second link: [to google](www.google.com)", TextType.TEXT),
                     TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) that should be all the links.", TextType.TEXT)
                     ]
        expected_nodes = [
            TextNode("This has two links. First link: ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "www.boot.dev"),
            TextNode(" and here is the second link: ", TextType.TEXT),
            TextNode("to google", TextType.LINK, "www.google.com"),
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            TextNode(" that should be all the links.", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_link(old_nodes), expected_nodes)

    def test_same_link_twice(self):
        old_nodes = [TextNode("This has two links. First link: [to boot dev](www.boot.dev) and here is the second link: [to google](www.google.com) This has two links. First link: [to boot dev](www.boot.dev) and here is the second link: [to google](www.google.com)", TextType.TEXT)]
        expected_nodes = [
            TextNode("This has two links. First link: ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "www.boot.dev"),
            TextNode(" and here is the second link: ", TextType.TEXT),
            TextNode("to google", TextType.LINK, "www.google.com"),
            TextNode(" This has two links. First link: ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "www.boot.dev"),
            TextNode(" and here is the second link: ", TextType.TEXT),
            TextNode("to google", TextType.LINK, "www.google.com")
            ]
        self.assertEqual(split_nodes_link(old_nodes), expected_nodes)

    def test_no_links(self):
        old_nodes = [TextNode("This is a text node with no links.", TextType.TEXT)]
        expected_nodes = [TextNode("This is a text node with no links.", TextType.TEXT)]
        self.assertEqual(split_nodes_link(old_nodes), expected_nodes)

    def test_no_surrounding_text(self):
        old_nodes = [TextNode("[to boot dev](www.boot.dev)[to google](www.google.com)", TextType.TEXT)]
        expected_nodes = [TextNode("to boot dev", TextType.LINK, "www.boot.dev"),
                          TextNode("to google", TextType.LINK, "www.google.com")
        ]
        self.assertEqual(split_nodes_link(old_nodes), expected_nodes)

    def test_blank_text(self):
        old_nodes = [TextNode("", TextType.TEXT)]
        expected_nodes = []
        self.assertEqual(split_nodes_link(old_nodes), expected_nodes)

    def test_space_text(self):
        old_nodes = [TextNode(" ", TextType.TEXT)]
        expected_nodes = [TextNode(" ", TextType.TEXT)]
        self.assertEqual(split_nodes_link(old_nodes), expected_nodes)

    def test_multiple_image_links(self):
        old_nodes = [TextNode("This has two links. First link: ![to boot dev](www.boot.dev) and here is the second link: ![to google](www.google.com)", TextType.TEXT)]
        expected_nodes = [
            TextNode("This has two links. First link: ", TextType.TEXT),
            TextNode("to boot dev", TextType.IMAGE, "www.boot.dev"),
            TextNode(" and here is the second link: ", TextType.TEXT),
            TextNode("to google", TextType.IMAGE, "www.google.com")
        ]
        self.assertEqual(split_nodes_image(old_nodes), expected_nodes)

    def test_multiple_images_with_multiple_nodes(self):
        old_nodes = [TextNode("This has two links. First link: ![to boot dev](www.boot.dev) and here is the second link: ![to google](www.google.com)", TextType.TEXT),
                     TextNode("This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)
                     ]
        expected_nodes = [
            TextNode("This has two links. First link: ", TextType.TEXT),
            TextNode("to boot dev", TextType.IMAGE, "www.boot.dev"),
            TextNode(" and here is the second link: ", TextType.TEXT),
            TextNode("to google", TextType.IMAGE, "www.google.com"),
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev"
            )
        ]
        self.assertEqual(split_nodes_image(old_nodes), expected_nodes)

    def test_multiple_images_with_multiple_nodes_text_at_end(self):
        old_nodes = [TextNode("This has two links. First link: ![to boot dev](www.boot.dev) and here is the second link: ![to google](www.google.com)", TextType.TEXT),
                     TextNode("This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev) that should be all the links.", TextType.TEXT)
                     ]
        expected_nodes = [
            TextNode("This has two links. First link: ", TextType.TEXT),
            TextNode("to boot dev", TextType.IMAGE, "www.boot.dev"),
            TextNode(" and here is the second link: ", TextType.TEXT),
            TextNode("to google", TextType.IMAGE, "www.google.com"),
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev"),
            TextNode(" that should be all the links.", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_image(old_nodes), expected_nodes)

    def test_splitting_markdown(self):
        markdown = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        expected = ["# This is a heading", 
                    "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                    "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
                    ]
        self.assertEqual(markdown_to_blocks(markdown),expected)

    def test_splitting_empty_blocks(self):
        markdown = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        expected = ["# This is a heading", 
                    "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                    "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
                    ]
        self.assertEqual(markdown_to_blocks(markdown),expected)

    def test_splitting_empty_blocks_with_spaces(self):
        markdown = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n         \n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        expected = ["# This is a heading", 
                    "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                    "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
                    ]
        self.assertEqual(markdown_to_blocks(markdown),expected)