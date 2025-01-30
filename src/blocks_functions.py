from important_functions import *


def markdown_to_blocks(markdown):
    new_blocks = []
    # Split on one or more blank lines
    # This handles various combinations of \n and whitespace
    blocks = markdown.split('\n')
    current_block = []
    
    for line in blocks:
        if line.strip() == '':
            if current_block:
                new_blocks.append('\n'.join(current_block))
                current_block = []
        else:
            current_block.append(line)
    
    if current_block:
        new_blocks.append('\n'.join(current_block))
    
    return new_blocks

def block_to_block_type(block):
    lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return "heading"
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return "code"
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return "paragraph"
        return "quote"
    if any(line.strip().startswith(("* ", "- ")) for line in lines):
        # Make sure all non-empty lines start with * or -
        for line in lines:
            if line.strip() and not line.strip().startswith(("* ", "- ")):
                return "paragraph"
        return "unordered_list"
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return "paragraph"
            i += 1
        return "ordered_list"
    return "paragraph"

def markdown_to_html_node(markdown):
    tags = {
        "code": "code",
        "quote": "blockquote",
        "unordered_list": "ul",
        "ordered_list": "ol",
        "paragraph": "p"
    }
    parent_node = HTMLNode("div")
    blocks = markdown_to_blocks(markdown)
    
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == "heading":
            heading_type = check_heading_type(block)
            node = HTMLNode(heading_type)
            cleaned_text = clean_blocks(block, block_type)
            node.children = text_to_children(cleaned_text)
        elif block_type == "code":
            node = HTMLNode("pre")
            code_node = HTMLNode("code")
            cleaned_text = clean_blocks(block, block_type)
            code_node.children = text_to_children(cleaned_text)
            node.children = [code_node]
        elif block_type in ["ordered_list", "unordered_list"]:
            node = HTMLNode(tags[block_type])
            items = clean_blocks(block, block_type)
            node.children = []
            for item in items:
                li_node = HTMLNode("li")
                li_node.children = text_to_children(item)
                node.children.append(li_node)
        else:
            node = HTMLNode(tags[block_type])
            cleaned_text = clean_blocks(block, block_type)
            node.children = text_to_children(cleaned_text)
            
        parent_node.children.append(node)
    return parent_node
    

def clean_blocks(text, block_type):
    if block_type == "heading":
        return text.lstrip("#").strip()
    elif block_type == "quote":
        lines = text.split("\n")
        cleaned_lines = []
        for line in lines:
            cleaned_lines.append(line.lstrip(">").strip())
        return "\n".join(cleaned_lines)
    elif block_type == "code":
        lines = text.split("\n")
        code_lines = lines[1:-1]
        return "\n".join(code_lines)
    elif block_type == "unordered_list":
        lines = text.split("\n")
        cleaned_ul_lines = []
        for line in lines:
            # Strip whitespace first, then check for markers
            stripped_line = line.strip()
            if stripped_line.startswith("*") or stripped_line.startswith("-"):
                # Remove the marker and any remaining whitespace
                cleaned_line = stripped_line[1:].strip()
                cleaned_ul_lines.append(cleaned_line)
        return cleaned_ul_lines
    elif block_type == "ordered_list":
        lines = text.split("\n")
        cleaned_ol_lines = []
        for line in lines:
            line = line.lstrip("0123456789").strip()
            line = line.lstrip(".").strip()
            cleaned_ol_lines.append(line)
        return cleaned_ol_lines
    elif block_type == "paragraph":
        return text.strip()
    else:
        return text
    
def check_heading_type(text):
    stripped = text.lstrip("#")
    level = len(text) - len(stripped)
    return f"h{level}"

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return HTMLNode("text", value=text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return HTMLNode("b", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return HTMLNode("i", value=text_node.text)
    elif text_node.text_type == TextType.CODE:
        return HTMLNode("code", value=text_node.text)
    elif text_node.text_type == TextType.LINK:
        return HTMLNode("a", value=text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return HTMLNode("img", props={"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError(f"Invalid text type: {text_node.text_type}")
    
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]
    