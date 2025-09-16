from typing import Optional
from enum import Enum

class TextType(Enum):
    TEXT = "plain text"
    BOLD = "bold text"
    ITALIC = "italic text"
    CODE = "code text"
    LINK = "link text"
    IMAGE = "image text"

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

    def __repr__(self):
        return f"{self.__class__.__name__}({self.text}, {self.text_type.value}, {self.url})"
