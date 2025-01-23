from .textnode import TextType, TextNode
from .htmlnode import *

def main():
    example_text_node = TextNode("This is a test node that should be pretty cool. +These words are bold+ but these words arent.", TextType.NORMAL)
    new_nodes = example_text_node.split_nodes_delimiter([example_text_node], "+", TextType.BOLD)
    print(new_nodes)
main()