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
    if block.startswith("```\n") and block.endswith("\n```"):
        return BlockType.CODE
    
    lines = block.splitlines()
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
    match block_type:
        case BlockType.HEADING:
            tag = get_heading_tag(block)
            value = block.split(" ", 1)[1]
            return LeafNode(tag, value)

        case BlockType.CODE:
            block = block.strip()
            lines = block.splitlines()
            if lines and lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            value = "\n".join(lines)
            return ParentNode("pre", [LeafNode("code", value)])

        case BlockType.QUOTE:
            block = block.strip()
            lines = block.splitlines()
            items = [line.strip("> ").strip() for line in lines if line.strip()]
            joined = " ".join(items)
            value = joined.strip()
            return LeafNode("blockquote", value)
                
        case BlockType.UNORDERED_LIST:
            block = block.strip()
            lines = block.splitlines()
            items = [line.strip("- ").strip() for line in lines if line.strip()]
            leaf_list = []
            for item in items:
                leaf_list.append(LeafNode("li", item))
            return ParentNode("ul", leaf_list)

        case BlockType.ORDERED_LIST:
            block = block.strip()
            lines = block.splitlines()
            items = [line.split(". ", 1)[1] for line in lines]
            leaf_list = []
            for item in items:
                leaf_list.append(LeafNode("li", item))
            return ParentNode("ol", leaf_list)

        case BlockType.PARAGRAPH:
            pass
            


