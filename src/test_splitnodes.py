from textnode import TextNode, TextType
from important_functions import split_nodes_delimiter, split_nodes_link, split_nodes_image, markdown_to_blocks, block_to_block_type
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

    def test_headings(self):
        markdown = "# This is a heading"
        expected = "heading"
        self.assertEqual(block_to_block_type(markdown), expected)

    def test_headings2(self):
        markdown = "## This is a heading"
        expected = "heading"
        self.assertEqual(block_to_block_type(markdown), expected)
    
    def test_headings_words_below(self):
        markdown = "# This is a heading\nThis is part of the block"
        expected = "heading"
        self.assertEqual(block_to_block_type(markdown), expected)

    def test_nothing_in_block(self):
        markdown = "This is a paragraph and shouldnt be anything else."
        excepted = "paragraph"
        self.assertEqual(block_to_block_type(markdown), excepted)

    def test_code_block(self):
        markdown = "``` This is a code block ```"
        excepted = "code"
        self.assertEqual(block_to_block_type(markdown), excepted)

    def test_code_block_multiple_lines(self):
        markdown = "``` This is a code block\nThis is part of a code block\nhere to this is```"
        excepted = "code"
        self.assertEqual(block_to_block_type(markdown), excepted)

    def test_code_block_multiple_lines_no_closing(self):
        markdown = "``` This is a code block\nThis is part of a code block\nhere to this is"
        excepted = "paragraph"
        self.assertEqual(block_to_block_type(markdown), excepted)

    def test_code_block_multiple_lines_no_opening(self):
        markdown = "This is a code block\nThis is part of a code block\nhere to this is```"
        excepted = "paragraph"
        self.assertEqual(block_to_block_type(markdown), excepted)

    def test_quote_block(self):
        markdown = "> This is part of a quote block\n>This is also part of a quote block\n> Even this is part of a quote block"
        excepted = "quote"
        self.assertEqual(block_to_block_type(markdown), excepted)

    def test_quote_block_missing_pointer(self):
        markdown = "> This is part of a quote block\nThis is also part of a quote block\n> Even this is part of a quote block"
        excepted = "paragraph"
        self.assertEqual(block_to_block_type(markdown), excepted)

    def test_ul_star(self):
        markdown = "* This is part of list\n* This is too\n* Same here"
        excepted = "unordered_list"
        self.assertEqual(block_to_block_type(markdown), excepted)

    def test_ul_dash(self):
        markdown = "- This is part of list\n- This is too\n- Same here"
        excepted = "unordered_list"
        self.assertEqual(block_to_block_type(markdown), excepted)
    
    def test_ul_missing_star_or_dash(self):
        markdown = "- This is part of list\n This is too\n- Same here"
        excepted = "paragraph"
        self.assertEqual(block_to_block_type(markdown), excepted)

    def test_ol(self):
        markdown = "1. This is part of list\n2. This is too\n3. Same here"
        excepted = "ordered_list"
        self.assertEqual(block_to_block_type(markdown), excepted)

    def test_ol_out_of_order(self):
        markdown = "2. This is part of list\n1. This is too\n3. Same here"
        excepted = "paragraph"
        self.assertEqual(block_to_block_type(markdown), excepted)

    def test_ol_no_first_number(self):
        markdown = "This is part of list\n1. This is too\n3. Same here"
        excepted = "paragraph"
        self.assertEqual(block_to_block_type(markdown), excepted)

    def test_ol_with_double_digit_numbers(self):
        markdown = "1. This is part of list\n2. This is too\n3. Same here\n4. This is part of list\n5. This is too\n6. Same here\n7. This is part of list\n8. This is too\n9. Same here\n10. This is part of list\n11. This is too\n12. Same here"
        excepted = "ordered_list"
        self.assertEqual(block_to_block_type(markdown), excepted)