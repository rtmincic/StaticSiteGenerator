from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    list_of_new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.NORMAL:
            list_of_new_nodes.append(node)
        else:
            if node.text.count(delimiter) % 2 == 0:
                split_node = node.text.split(delimiter)
                for i in range(0, len(split_node)):
                    if i % 2 == 0:
                        list_of_new_nodes.append(TextNode(split_node[i], TextType.NORMAL))
                    else:
                        list_of_new_nodes.append(TextNode(split_node[i], text_type))
            else:
                raise Exception("There is a missing closing delimiter")
    return list_of_new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)" , text)