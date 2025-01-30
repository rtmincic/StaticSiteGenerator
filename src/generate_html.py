from markdown_blocks import markdown_to_html_node
import os

def extract_title(markdown):
    line = markdown.split("\n", 1)
    if line[0].startswith("# "):
        first_line = line[0].lstrip("#").strip()
    else: 
        raise Exception("No header or Not an h1 header")
    return first_line

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as file:
        content = file.read()
    with open(template_path, "r") as template_file:
        template_content = template_file.read()
    title = extract_title(content)
    html = markdown_to_html_node(content)
    print(html)
    html = html.to_html()
    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", html)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as output_file:
        output_file.write(template_content)
