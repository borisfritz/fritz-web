from typing import Optional
from enum import Enum

from .htmlnode import LeafNode

class TextType(Enum):
    TEXT = "plain-text"
    BOLD = "bold-text"
    ITALIC = "italic-text"
    CODE = "code-text"
    LINK = "link-text"
    IMAGE = "image-text"

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: Optional[str]=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, o):
        if not isinstance(o, type(self)):
            return NotImplemented
        return (
            self.text == o.text and
            self.text_type == o.text_type and
            self.url == o.url
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(node: TextNode) -> LeafNode:
    match node.text_type:
        case TextType.TEXT:
            return LeafNode(None, node.text)
        case TextType.BOLD:
            return LeafNode("b", node.text)
        case TextType.ITALIC:
            return LeafNode("i", node.text)
        case TextType.CODE:
            return LeafNode("code", node.text)
        case TextType.LINK:
            return LeafNode("a", node.text, {"href": node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": node.url, "alt": node.text})
        case _:
            raise ValueError(f"invalid text type: {node.text_type}")
