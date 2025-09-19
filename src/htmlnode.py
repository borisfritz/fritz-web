from typing import List, Dict, Optional

class HTMLNode:
    def __init__(
        self,
        tag: Optional[str]=None,
        value: Optional[str]=None,
        children: Optional[List]=None,
        props: Optional[Dict[str,str]]=None
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self) -> str:
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

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: List["LeafNode"],
        props: Optional[Dict[str,str]]=None,
    ):
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("argument 'tag' is required in ParentNode!")
        if not self.children:
            raise ValueError("argument 'children' is required in ParentNode!")

        result = ""
        for node in self.children:
            node_result = node.to_html()
            result += node_result

        props = ""
        if self.props:
            props = self.props_to_html()
        return f'<{self.tag}{props}>{result}</{self.tag}>'

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.tag}, {self.children}, {self.props})"
