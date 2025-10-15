import re

from .textnode import TextType, TextNode

def text_to_textnodes(text: str) -> list[TextNode]:
    if not text:
        raise ValueError("Invalid Input 'text' argument.")
    results = [TextNode(text, TextType.TEXT)]
    results = split_nodes_image_link(results)
    results = split_nodes_image(results)
    results = split_nodes_link(results)
    results = split_nodes_delimiter(results, "`", TextType.CODE)
    results = split_nodes_delimiter(results, "**", TextType.BOLD)
    results = split_nodes_delimiter(results, "_", TextType.ITALIC)
    return results

def split_nodes_delimiter(
    old_nodes: list[TextNode],
    delimiter: str,
    text_type: TextType
) -> list[TextNode]:

    results = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            results.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise Exception(f"Invalid markdown syntax, unclosed delimiter: {delimiter} in part: {parts}")
        for i, part in enumerate(parts):
            if i % 2 == 0:
                if part != "":
                    paragraph = " ".join(part.splitlines())
                    results.append(TextNode(paragraph, TextType.TEXT))
            else:
                results.append(TextNode(part, text_type))
    return results

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    results = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            results.append(node)
            continue

        img_text = extract_markdown_images(node.text)
        if not img_text:
            results.append(node)
            continue

        remainder = node.text
        for alt, url in img_text:
            left, remainder = remainder.split(f"![{alt}]({url})", 1)
            if left:
                results.append(TextNode(left, TextType.TEXT))
            results.append(TextNode(alt, TextType.IMAGE, url))
        if remainder:
            results.append(TextNode(remainder, TextType.TEXT))
    return results

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    results = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            results.append(node)
            continue

        link_text = extract_markdown_links(node.text)
        if not link_text:
            results.append(node)
            continue

        remainder = node.text
        for text, href in link_text:
            left, remainder = remainder.split(f"[{text}]({href})", 1)
            if left:
                results.append(TextNode(left, TextType.TEXT))
            results.append(TextNode(text, TextType.LINK, href))
        if remainder:
            results.append(TextNode(remainder, TextType.TEXT))
    return results

def split_nodes_image_link(old_nodes: list[TextNode]) -> list[TextNode]:
    results = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            results.append(node)
            continue
        img_link_data = extract_markdown_image_links(node.text)
        if not img_link_data:
            results.append(node)
            continue
        remainder = node.text
        for alt, img_url, link_url in img_link_data:
            full_syntax = f"[![{alt}]({img_url})]({link_url})"
            left, remainder = remainder.split(full_syntax, 1)
            if left:
                results.append(TextNode(left, TextType.TEXT))
            results.append(TextNode(f"{alt}||LINK||{link_url}", TextType.IMAGE, img_url))
        if remainder:
            results.append(TextNode(remainder, TextType.TEXT))
    return results

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_image_links(text: str) -> list[tuple[str, str, str]]:
    pattern = r"\[!\[([^\]]*)\]\(([^\)]*)\)\]\(([^\)]*)\)"
    matches = re.findall(pattern, text)
    return matches
