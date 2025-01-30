from textnode import TextType, TextNode
from htmlnode import *
from important_functions import *
from blocks_functions import *

def main():
    text = """* First item with some *italic* text
- Second item with some **bold** text
* Third item with some `code`
- Fourth item with multiple
* Fifth item has a *nested* **style**"""
    cleaned = clean_blocks(text, "unordered_list")
    textnodes = text_to_textnodes(cleaned)
    print(textnodes)



main()