from typing import List, Dict, Optional

class HTMLNode:
    def __init__(
        self,
        tag: Optional[str]=None,
        value: Optional[str]=None,
        children: Optional[List["HTMLNode"]]=None,
        props: Optional[Dict[str,str]]=None
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if self.props is None:
            return ""
        else:
            return "".join(f' {k}="{v}"' for k, v in self.props.items())

    def __repr__(self):
        return f"{self.__class__.__name__}({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        value: str,
        props: Optional[Dict[str,str]]=None
    ):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("LeafNode must have self.value")
        if not self.tag:
            return self.value
        else:
            props = ""
            if self.props:
                props = self.props_to_html()
            return f'<{self.tag}{props}>{self.value}</{self.tag}>'

    def __repr__(self):
        return f"{self.__class__.__name__}({self.tag}, {self.value}, {self.props})"
