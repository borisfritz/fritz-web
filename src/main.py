from textnode import TextNode, TextType
from htmlnode import HTMLNode

def main():
    props = {"href": "boot.dev", "src": "asset/image/suffer.jpg", "alt": "you will suffer in this class!"}
    node = HTMLNode(None, None, None, props)
    print(node.props_to_html())

if __name__ == "__main__":
    main()
