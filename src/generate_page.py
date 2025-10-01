import os

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
