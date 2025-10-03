from enum import Enum
from src.htmlnode import LeafNode, ParentNode, HTMLNode
from src.inline_markdown import text_to_textnodes
from src.textnode import text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered-list"
    ORDERED_LIST = "ordered-list"

def markdown_to_html_node(markdown: str):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = get_blocktype(block)
        html_nodes.append(block_to_htmlnode(block, block_type))
    return ParentNode("div", html_nodes)

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    stripped = list(map(str.strip, blocks))
    results = []
    for block in stripped:
        if block != "":
            results.append(block)
    return results

def get_blocktype(block: str) -> BlockType:
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    lines = block.splitlines()
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    if all(line.split(". ")[0].isdigit() and int(line.split(".", 1)[0]) == i + 1 for i, line in enumerate(lines)):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def get_heading_tag(block: str) -> str:
    if block.startswith("# "):
        return "h1"
    if block.startswith("## "):
        return "h2"
    if block.startswith("### "):
        return "h3"
    if block.startswith("#### "):
        return "h4"
    if block.startswith("##### "):
        return "h5"
    if block.startswith("###### "):
        return "h6"

def block_to_htmlnode(block: str, block_type: BlockType):
    match block_type:
        case BlockType.HEADING:
            tag = get_heading_tag(block)
            value = block.split(" ", 1)[1]
            return LeafNode(tag, value)

        case BlockType.CODE:
            block = block.strip()
            lines = block.splitlines()
            if lines and lines[0].startswith("```") and lines[-1].endswith("```"):
                lines = lines[1:-1]
            value = "\n".join(lines)
            return ParentNode("pre", [LeafNode("code", value)])

        case BlockType.QUOTE:
            block = block.strip()
            lines = block.splitlines()
            result = []
            for line in lines:
                html_nodes = []
                if line.strip():
                    split = line.split(" ", 1)
                    if len(split) == 1:
                        result.append("")
                        continue
                    text = split[1]
                    text_nodes = text_to_textnodes(text)
                    for node in text_nodes:
                        html_nodes.append(text_node_to_html_node(node))
                    inline = ""
                    for node in html_nodes:
                        inline += node.to_html()
                    result.append(inline)
            final = "\n".join(result)
            return LeafNode("blockquote", final)
                
        case BlockType.UNORDERED_LIST:
            block = block.strip()
            lines = block.splitlines()
            children = []
            for line in lines:
                html_nodes = []
                if line.strip():
                    text = line.split(" ", 1)[1]
                    text_nodes = text_to_textnodes(text)
                    for node in text_nodes:
                        html_nodes.append(text_node_to_html_node(node))
                    result = ""
                    for node in html_nodes:
                        result += node.to_html()
                    children.append(LeafNode("li", result))
            return ParentNode("ul", children)

        case BlockType.ORDERED_LIST:
            block = block.strip()
            lines = block.splitlines()
            children = []
            for line in lines:
                html_nodes = []
                if line.strip():
                    text = line.split(". ", 1)[1]
                    text_nodes = text_to_textnodes(text)
                    for node in text_nodes:
                        html_nodes.append(text_node_to_html_node(node))
                    result = ""
                    for node in html_nodes:
                        result += node.to_html()
                    children.append(LeafNode("li", result))
            return ParentNode("ol", children)

        case BlockType.PARAGRAPH:
            block = block.strip()
            text_nodes = text_to_textnodes(block)
            html_nodes = []
            for node in text_nodes:
                html_nodes.append(text_node_to_html_node(node))
            return ParentNode("p", html_nodes)

        case _:
            raise AttributeError("Invalid BlockType")

