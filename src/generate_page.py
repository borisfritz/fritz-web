import os
from pathlib import Path

from src.block_markdown import markdown_to_html_node

def extract_title(markdown: str) -> str:
    lines = markdown.splitlines()
    if lines[0].startswith("# "):
        return lines[0].split(" ", 1)[1]
    else:
        raise Exception("No Header found in .md file! File must start with '# title'")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating Page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        md_file = f.read()
    with open(template_path, "r") as f:
        template_file = f.read()
    title = extract_title(md_file)
    html_string = markdown_to_html_node(md_file).to_html()
    result = template_file.replace("{{ Title }}", title)
    result = result.replace("{{ Content }}", html_string)
    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(result)

def generate_website(content_dir_path, template_path, dest_dir_path):
    for item in os.listdir(content_dir_path):
        c_item = os.path.join(content_dir_path, item)
        d_item = os.path.join(dest_dir_path, item)
        if os.path.isdir(c_item):
            os.makedirs(d_item)
            print(f"Created Directory: {d_item}")
            generate_website(c_item, template_path, d_item)
        elif item.lower().endswith(".md"):
            h_name = os.path.splitext(item)[0] +".html"
            h_item = os.path.join(dest_dir_path, h_name)
            generate_page(c_item, template_path, h_item)
            print(f"Generated File: {c_item} -> {d_item}")
