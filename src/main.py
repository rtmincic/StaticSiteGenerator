from textnode import TextType, TextNode
from htmlnode import *
from important_functions import split_nodes_delimiter

def main():
    old_nodes = [TextNode("This |is| a |test", TextType.NORMAL)]
    expected_nodes = [
            TextNode("This ", TextType.NORMAL),
            TextNode("is", TextType.BOLD),
            TextNode(" a ", TextType.NORMAL),
            TextNode("test", TextType.BOLD),
            TextNode("", TextType.NORMAL),  # Trailing empty node
        ]
    
    split_nodes_delimiter(old_nodes,"|", TextType.BOLD)
    print("There is a missing closing delimiter")
main()