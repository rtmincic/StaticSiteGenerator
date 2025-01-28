from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    list_of_new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            list_of_new_nodes.append(node)
        else:
            if node.text.count(delimiter) % 2 == 0:
                split_node = node.text.split(delimiter)
                for i in range(0, len(split_node)):
                    if i % 2 == 0:
                        list_of_new_nodes.append(TextNode(split_node[i], TextType.TEXT))
                    else:
                        list_of_new_nodes.append(TextNode(split_node[i], text_type))
            else:
                raise Exception("There is a missing closing delimiter")
    return list_of_new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)" , text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_bold(text):
    return re.findall(r"\*\*(.*?)\*\*", text)

def extract_markdown_italics(text):
    return re.findall(r"\*(.*?)\*", text)

def extract_markdown_code(text):
    return re.findall(r"\`(.*?)\`", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0 and old_node.text != "":
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0  and old_node.text != "":
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    orginal_node = [TextNode(text, TextType.TEXT)]
    image_check = extract_markdown_images(text)
    link_check = extract_markdown_links(text)
    bold_check = extract_markdown_bold(text)
    italic_check = extract_markdown_italics(text)
    code_check = extract_markdown_code(text)
    if image_check:
        orginal_node = split_nodes_image(orginal_node)
    if link_check:
        updated_list = []
        for node in orginal_node:
            if node.text_type == TextType.TEXT:
                split_links = split_nodes_link([node])
                for linknode in split_links:
                    updated_list.append(linknode)
            else:
                updated_list.append(node)
    orginal_node = updated_list
    if bold_check:
        orginal_node = process_delimiters(orginal_node, "**", TextType.BOLD)
    if italic_check:
        orginal_node = process_delimiters(orginal_node, "*", TextType.ITALIC)
    if code_check:
        orginal_node = process_delimiters(orginal_node, "`", TextType.CODE)
    return orginal_node

def process_delimiters(orginal_node, delimiter, text_type):
    updated_list = []
    for node in orginal_node:
        if node.text_type == TextType.TEXT:
            split_nodes = split_nodes_delimiter([node], delimiter, text_type)
            updated_list.extend(split_nodes)
        else:
            updated_list.append(node)
    return updated_list

def markdown_to_blocks(markdown):
    new_blocks = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        temp_block = block.strip()
        if temp_block:
            new_blocks.append(temp_block)
    return new_blocks