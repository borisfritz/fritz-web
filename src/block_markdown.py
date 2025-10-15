import re
from enum import Enum
from src.htmlnode import LeafNode, ParentNode
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
        block_type = get_block_type(block)
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

def get_block_type(block: str) -> BlockType:
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    lines = block.splitlines()
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.lstrip().startswith(("- ", "* ", "+ ")) for line in lines):
        return BlockType.UNORDERED_LIST
    matches = [re.match(r'^\s*(\d+)\.\s', line) for line in lines]
    if all(matches):
        top_level_items = [(int(match.group(1)), line) for match, line in zip(matches, lines) if not line.startswith((' ', '\t'))]
        if top_level_items:
            top_level_numbers = [num for num, _ in top_level_items]
            if top_level_numbers == list(range(1, len(top_level_numbers) + 1)):
                return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def get_heading_tag(block: str) -> str | None:
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
    return None

def parse_list_items(lines: list[str], is_ordered: bool) -> list[dict]:
    items = []
    stack = []
    for line in lines:
        if not line.strip():
            continue
        expanded_line = line.expandtabs(4)
        indent = len(expanded_line) - len(expanded_line.lstrip())
        level = indent // 2
        if is_ordered:
            match = re.match(r'^\s*\d+\.\s+(.*)$', line)
            if match:
                text = match.group(1)
            else:
                continue
        else:
            match = re.match(r'^\s*[-*+]\s+(.*)$', line)
            if match:
                text = match.group(1)
            else:
                continue
        item = {'text': text.strip(), 'level': level, 'children': []}
        while stack and stack[-1]['level'] >= level:
            stack.pop()
        if stack:
            stack[-1]['children'].append(item)
        else:
            items.append(item)
        stack.append(item)
    return items

def build_list_html_nodes(items: list[dict], is_ordered: bool) -> list:
    children = []
    for item in items:
        text_html = text_to_html(item['text'])
        if item['children']:
            nested_list = build_list_html_nodes(item['children'], is_ordered)
            tag = "ol" if is_ordered else "ul"
            nested_node = ParentNode(tag, nested_list)
            li_children = [LeafNode(None, text_html), nested_node]
            children.append(ParentNode("li", li_children))
        else:
            children.append(LeafNode("li", text_html))
    return children

def text_to_html(text):
    html_nodes = []
    text_nodes = text_to_textnodes(text)
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    result = ""
    for node in html_nodes:
        result += node.to_html()
    return result

def block_to_htmlnode(block: str, block_type: BlockType):
    match block_type:
        case BlockType.HEADING:
            tag = get_heading_tag(block)
            text = block.split(" ", 1)[1]
            result = text_to_html(text)
            return LeafNode(tag, result)

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
            quote_block = []
            for line in lines:
                if line.strip():
                    split = line.split(" ", 1)
                    if len(split) == 1:
                        quote_block.append("")
                        continue
                    text = split[1]
                    result = text_to_html(text)
                    quote_block.append(result)
            final = "\n".join(quote_block)
            return LeafNode("blockquote", final)
                
        case BlockType.UNORDERED_LIST:
            block = block.strip()
            lines = block.splitlines()
            items = parse_list_items(lines, False)
            children = build_list_html_nodes(items, False)
            return ParentNode("ul", children)

        case BlockType.ORDERED_LIST:
            block = block.strip()
            lines = block.splitlines()
            items = parse_list_items(lines, True)
            children = build_list_html_nodes(items, True)
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