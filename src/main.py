from textnode import TextType, TextNode
from htmlnode import *
from important_functions import text_to_textnodes, extract_markdown_bold, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
import re

def main():
    text = "this text has a little of everything **this is bold** here is an image ![to boot dev](www.boot.dev) and *this is in italics* here is a link [to google](www.google.com) finally `this is a code` that should be everything"
    everything_split = text_to_textnodes(text)
    print(everything_split)

main()