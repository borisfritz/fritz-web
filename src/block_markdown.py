from enum import Enum
from src.htmlnode import LeafNode, ParentNode, HTMLNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered-list"
    ORDERED_LIST = "ordered-list"

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    stripped = list(map(str.strip, blocks))
    results = []
    for block in stripped:
        if block != "":
            results.append(block)
    return results

def block_to_blocktype(block: str) -> BlockType:
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    lines = block.split("\n")
    if all(line.startswith("> ") for line in lines):
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
    match BlockType:
        case BlockType.HEADING:
            tag = get_heading_tag(block)
            value = block.split(" ", 1)[1]
            return LeafNode(tag, value)

        case BlockType.CODE:
            value = block.strip("```")
            return ParentNode("pre", [LeafNode("code", value)])

        case BlockType.QUOTE:
            lines = block.split("\n")
            for line in lines:
                line.strip(">")
            value = "".join(lines)
            return LeafNode("blockquote", value)
                
        case BlockType.UNORDERED_LIST:
            lines = block.splitlines()
            items = [line.lstrip("- ").strip() for line in lines if line.strip()]
            wrapped = [f"<li>{item}</li>" for item in items]
            value = "\n".join(wrapped)
            return ParentNode("ul", LeafNode(""))


        case BlockType.ORDERED_LIST:
            pass

        case BlockType.PARAGRAPH:
            pass
