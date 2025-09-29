from src.block_markdown import BlockType
from src.block_markdown import markdown_to_blocks, get_blocktype, block_to_htmlnode
from src.htmlnode import ParentNode, LeafNode

def markdown_do_html_node(markdown: str):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_blocktype(block)
