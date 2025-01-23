from textnode import *
from htmlnode import *

def main():
    textNode = TextNode("This is some text", TextType.NORMAL, "https://www.boot.dev")
    print(textNode)
    node = ParentNode("p",
                          [LeafNode("b", "Bold Text"),
                          ParentNode("p",[
                                     LeafNode("i", "Italic text"),
                                     LeafNode("h1", "Header text")
                          ]),
                          LeafNode("a", "Link Text")  
                          ]
                          )

    print(node.to_html())


main()