from textnode import TextType, TextNode
from htmlnode import *
from important_functions import text_to_textnodes, extract_markdown_bold, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, block_to_block_type
import re

def main():
    heading1 = "# This is a heading"
    heading2 = "## This is also a heading"
    notheading = "This is not a heading"
    code_block = "``` This is a code block ```"
    quote_block = "> This is part of a quote block\nThis is also part of a quote block\n> Even this is part of a quote block"
    ul_list = "* This is part of list\nThis is too\n* Same here"
    ol = "1. This is part of an ordered list\n\t2. This is also part of an ordered list\n3. This is too"

   
    

    print(block_to_block_type(ol))


main()